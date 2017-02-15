import wave
import functools
import itertools
from enum import Enum
from enum import IntEnum
import pprint
import sys

import webrtcvad
import numpy as np

def _normalize(signal):
    scale = np.absolute(signal).max()
    return (1/scale) * signal


def _split(x, n, trim=False):
    chunks = [x[i:i+n] for i in range(0, len(x), n)]
    if trim and len(chunks[-1]) < n:
        return chunks[:-1]
    return chunks


class Mask:
    def __init__(self, *, mask, frame_duration):
        #mask true when the frame is speech
        self.mask = mask
        self.frame_duration = frame_duration
        self.delta = self.frame_duration / 1000

    def __str__(self):
        return str(self.mask)

    @functools.lru_cache()
    def _count_silence_frames(self):
        return self.mask.count(False)

    def _count_speech_frames(self):
        return len(self.mask) - self._count_silence_frames();

    @property
    def silence_duration(self):
        return self._count_silence_frames() * self.delta

    @property
    def silence_to_total_ratio(self):
        return self._count_silence_frames() / len(self.mask)

    @functools.lru_cache()
    def count_segments(self):
        return [(value, sum(1 for _ in group)) for value, group in itertools.groupby(self.mask)]

    @property
    def longest_silence_segment_duration(self):
        count = max(v[1] for v in self.count_segments() if v[0])
        return count * self.delta

    @property
    def longest_speech_segment_duration(self):
        count = max(v[1] for v in self.count_segments() if not v[0])
        return count * self.delta

    @property
    def segments_amount(self):
        return len([_ for value, group in itertools.groupby(self.mask) if value])

    # boolean and for mask vectors for argument
    @classmethod
    def intersect(cls, first, second):
        assert first.frame_duration == second.frame_duration
        assert len(first.mask) == len(second.mask)

        return cls(mask=[a or b for a, b in zip(first.mask, second.mask)],
                   frame_duration=first.frame_duration)

    @property
    def speech_duration(self):
        return self._count_speech_frames() * self.delta

    @property
    def speech_to_total_ratio(self):
        return self._count_speech_frames() / len(self.mask)

    def frames_to_ratio(self, frames_count):
        return frames_count / len(self.mask)

    def frames_to_duration(self, frames_count):
        return frames_count * self.delta


class Track:
    def __init__(self, bytes, *, sampwidth, framerate):
        self.bytes = bytes
        self.sampwidth = sampwidth
        self.framerate = framerate

        assert self.sampwidth == 2  # only 2 bytes (16 bits) per sample
        assert self.framerate in [8000, 16000]

        self.signal = _normalize(np.fromstring(self.bytes, dtype=np.int16))

    @classmethod
    def from_file(cls, filename, channel=None):
        with wave.open(filename, 'rb') as container:
            meta = container.getparams()
            bytes_ = container.readframes(meta.nframes)  # Read the whole file

        assert meta.nchannels in [1, 2]
        assert meta.comptype == 'NONE'  # No compression

        if meta.nchannels == 1:
            binary = bytes_
        else:
            # Dealing with stereo format.
            assert channel in [0, 1]
            chunks = _split(bytes_, meta.sampwidth)
            assert len(chunks[-1]) == meta.sampwidth
            span = slice(channel, None, 2)  # equvivalent to [0::2] or [1::2]
            binary = b''.join(chunks[span])

        return cls(binary, sampwidth=meta.sampwidth, framerate=meta.framerate)

    @property
    def duration(self):
        """Get track duration in seconds."""
        return (len(self.bytes) / self.sampwidth) / self.framerate

    @property
    def delta(self):
        return 1 / self.framerate

    def _get_frames(self, frame_duration):
        # frame_duration is in [ms].
        bytes_per_frame = int(
            self.sampwidth * self.framerate * frame_duration / 1000
        )
        return _split(self.bytes, bytes_per_frame, trim=True)

    def get_mask(self, vad_agressiviness_level, frame_duration=30):
        """Frame duration is in ms."""
        assert frame_duration in [10, 20, 30]
        frames = self._get_frames(frame_duration=frame_duration)

        vad = webrtcvad.Vad(mode=vad_agressiviness_level)

        mask = [vad.is_speech(frame, self.framerate) for frame in frames]

        return Mask(mask=mask, frame_duration=frame_duration)

    @classmethod
    def same_format(cls, first, second):
        return (first.framerate, first.sampwidth) == (second.framerate, second.sampwidth)

class SpeechState(IntEnum):
    OPERATOR = 1
    CLIENT = 2
    SILENCE = 0
    INTERRUPTION = 3

    @staticmethod
    def fromMasks(cl, op):
        if op and cl:
            return SpeechState.INTERRUPTION
        if op:
            return SpeechState.OPERATOR
        if cl:
            return SpeechState.CLIENT
        return SpeechState.SILENCE

class Dialog:

    def __init__(self, track_client, track_operator, *, freezingLimit = 5, vad_agressiviness_level = 3, frame_duration = 30):

        track_1, track_2 = track_client, track_operator
        assert Track.same_format(track_1, track_2)

        common_length = min(len(track_1.bytes), len(track_2.bytes))

        factory = functools.partial(Track,
                                    sampwidth=track_1.sampwidth,
                                    framerate=track_1.framerate)

        self.track_client = factory(track_1.bytes[:common_length])
        self.track_operator = factory(track_2.bytes[:common_length])

        self.mask_client = self.track_client.get_mask(vad_agressiviness_level, frame_duration)
        self.mask_operator = self.track_operator.get_mask(vad_agressiviness_level, frame_duration)

        self.mask_both = Mask.intersect(self.mask_client, self.mask_operator)
        self.freezingLimit = freezingLimit

    def frames_to_ratio(self, frames_count):
        return self.mask_client.frames_to_ratio(frames_count)

    def frames_to_duration(self, frames_count):
        return self.mask_client.frames_to_ratio(frames_count)

    def influence_iterator(self):
        cur = SpeechState.fromMasks(self.mask_client.mask[0], self.mask_operator.mask[0])
        prev = SpeechState.SILENCE
        duration = 0
        for cl, op in zip(self.mask_client.mask, self.mask_operator.mask):
            if cur != SpeechState.fromMasks(cl, op):
                if duration:
                    yield (cur, prev, duration)
                prev = cur
                cur = SpeechState.fromMasks(cl, op)
                duration = 1
            else:
                duration += 1

    def get_silence_info(self):
        data = {}
        for name, mask in zip(('client', 'operator', 'both'),
                              (self.mask_client, self.mask_operator, self.mask_both)):
            data[name] = {
                'silence_duration': mask.silence_duration,
                'silence_to_total_ratio': mask.silence_to_total_ratio,
                'longest_silence_segment_duration': mask.longest_silence_segment_duration,
                'longest_speech_segment_duration' : mask.longest_speech_segment_duration,
                'speech_to_total_ratio' : mask.speech_to_total_ratio,
                'speech_duration' : mask.speech_duration
            }
        data['operator_to_client_speech_ratio'] = data['operator']['speech_duration'] / data['client']['speech_duration']
        return data

    def get_interruptions_info(self) :
        client = 0
        operator = 0
        both = 0
        clientFrames = 0
        operatorFrames = 0
        bothFrames = 0
        clientFreezing = 0
        operatorFreezing = 0
        for interruption in self.influence_iterator():
            if interruption[0] is SpeechState.INTERRUPTION:
                if interruption[1] is SpeechState.CLIENT:
                    client += 1
                    clientFrames += interruption[2]
                elif interruption[1] is SpeechState.OPERATOR:
                    operator += 1
                    operatorFrames += interruption[2]
                both += 1
                bothFrames += interruption[2]
            elif interruption[0] is SpeechState.SILENCE:
                dur = self.frames_to_duration(interruption[2])
                if interruption[1] is SpeechState.CLIENT or interruption[1] is SpeechState.INTERRUPTION:
                    if dur > self.freezingLimit:
                        operatorFreezing += dur
                if interruption[1] is SpeechState.OPERATOR or interruption[1] is SpeechState.INTERRUPTION:
                    if dur > self.freezingLimit:
                        clientFreezing += dur

        return {
            'client' : {
                'count' : client,
                'duration' : self.frames_to_duration(clientFrames),
                'ratio' : self.frames_to_ratio(clientFrames),
                'freezing' : clientFreezing
            },
            'operator' : {
                'count' : operator,
                'duration' : self.frames_to_duration(operatorFrames),
                'ratio' : self.frames_to_ratio(operatorFrames),
                'freezing' : operatorFreezing
            },
            'both' : {
                'count' : both,
                'duration' : self.frames_to_duration(bothFrames),
                'ratio' : self.frames_to_ratio(bothFrames)
            }
        }



if __name__ == '__main__':

    filename = './audio_samples/Dialog_1/dialog.wav'
    tr_1 = Track.from_file(filename, channel=0)
    tr_2 = Track.from_file(filename, channel=1)
    dialog = Dialog(track_client=tr_1, track_operator=tr_2)

    silence_info = dialog.get_silence_info()
    interruptions_info = dialog.get_interruptions_info()
    # pprint.pprint(info)

    result = (
        'Речь оператора, %                             {9:>6.2f}\n'
        'Речь клиента, %                               {10:>6.2f}\n'
        'Речь оператора, сек                           {11:>6.2f}\n'
        'Речь клиента, сек                             {12:>6.2f}\n\n'
        'Отношение речи оператора к речи клиента       {13:>6.2f}\n'
        'Максимальный участок речи клиента, сек        {14:>6.2f}\n'
        'Максимальный участок речи оператора, сек      {15:>6.2f}\n\n\n'
        'Перебивания, %                                {16:>6.2f}\n'
        'Перебивания, шт                               {17:>6d}\n'
        'Перебивания, сек                              {18:>6.2f}\n\n'
        'Перебивания клиента оператором, %             {19:>6.2f}\n'
        'Перебивания клиента оператором, шт            {20:>6d}\n'
        'Перебивания клиента оператором, сек           {21:>6.2f}\n\n'
        'Перебивания оператора клиентом, %             {22:>6.2f}\n'
        'Перебивания оператора клиентом, шт            {23:>6d}\n'
        'Перебивания оператора клиентом, сек           {24:>6.2f}\n\n\n'
        'Общая продолжительность молчания, %:          {0:>6.2f}\n'
        'Общая продолжительность молчания, сек:        {1:>6.2f}\n'
        'Максимальный участок молчания, сек:           {2:>6.2f}\n\n'
        'Продолжительность молчания оператора, %:      {3:>6.2f}\n'
        'Продолжительность молчания оператора, сек:    {4:>6.2f}\n'
        'Максимальный участок молчания оператора, сек: {5:>6.2f}\n\n'
        'Продолжительность молчания клиента, %:        {6:>6.2f}\n'
        'Продолжительность молчания клиента, сек:      {7:>6.2f}\n'
        'Максимальный участок молчания клиента, сек:   {8:>6.2f}\n'
        'Залипания оператора (паузы более 5-10 секунд после реплики клиента), сек\t{25:>6.7f}\n'
        'Залипания клиента (паузы более 5-10 секунд после реплики оператора), сек\t{26:>6.7f}\n'
    ).format(
        silence_info['both']['silence_to_total_ratio'] * 100,
        silence_info['both']['silence_duration'],
        silence_info['both']['longest_silence_segment_duration'],
        silence_info['operator']['silence_to_total_ratio'] * 100,
        silence_info['operator']['silence_duration'],
        silence_info['operator']['longest_silence_segment_duration'],
        silence_info['client']['silence_to_total_ratio'] * 100,
        silence_info['client']['silence_duration'],
        silence_info['client']['longest_silence_segment_duration'],
        silence_info['client']  ['speech_to_total_ratio'] * 100,
        silence_info['operator']['speech_to_total_ratio'] * 100,
        silence_info['client']  ['speech_duration'],
        silence_info['operator']['speech_duration'],
        silence_info['operator_to_client_speech_ratio'],
        silence_info['client']  ['longest_speech_segment_duration'],
        silence_info['operator']['longest_speech_segment_duration'],
        interruptions_info['both']['ratio'] * 100,
        interruptions_info['both']['count'],
        interruptions_info['both']['duration'],  
        interruptions_info['client']['ratio'] * 100,
        interruptions_info['client']['count'],
        interruptions_info['client']['duration'],  
        interruptions_info['operator']['ratio'] * 100,
        interruptions_info['operator']['count'],
        interruptions_info['operator']['duration'],
        interruptions_info['client']['freezing'], 
        interruptions_info['operator']['freezing'],        
    )

    print()
    print(result)
