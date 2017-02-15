import wave
import functools
import itertools
from enum import Enum
import pprint

import webrtcvad
import numpy as np

VAD_AGRESSIVINESS_LEVEL = 3  # 0, 1, 2, 3

MaskType = Enum('MaskType', 'SPEECH, SILENCE')


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
        #mask true when the frame is silance
        self.mask = mask
        self.frame_duration = frame_duration
        self.delta = self.frame_duration / 1000

    def __str__(self):
        return str(self.mask)

    @functools.lru_cache()
    def _count_silence_frames(self):
        return self.mask.count(True)

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
        return [(value, len(list(group))) for value, group in itertools.groupby(self.mask)]

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

        return cls(mask=[a and b for a, b in zip(first.mask, second.mask)],
                   frame_duration=first.frame_duration)

    @property
    def speech_duration(self):
        return self._count_speech_frames() * self.delta

    @property
    def speech_to_total_ratio(self):
        return self._count_speech_frames() / len(self.mask)


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

    def get_mask(self, mask_type, frame_duration=30):
        """Frame duration is in ms."""
        assert frame_duration in [10, 20, 30]
        frames = self._get_frames(frame_duration=frame_duration)

        vad = webrtcvad.Vad(mode=VAD_AGRESSIVINESS_LEVEL)

        def crit(frame):
            is_speech = vad.is_speech(frame, self.framerate)
            return is_speech is (mask_type is MaskType.SPEECH)

        mask = [crit(frame) for frame in frames]
        return Mask(mask=mask, frame_duration=frame_duration)

    @classmethod
    def same_format(cls, first, second):
        return (first.framerate, first.sampwidth) == (second.framerate, second.sampwidth)

class Interruption:
    def __init__(self, from_operator, duration):
        self.from_operator = from_operator
        self.duration = duration

class Dialog:

    def __init__(self, track_client, track_operator):

        track_1, track_2 = track_client, track_operator
        assert Track.same_format(track_1, track_2)

        common_length = min(len(track_1.bytes), len(track_2.bytes))

        factory = functools.partial(Track,
                                    sampwidth=track_1.sampwidth,
                                    framerate=track_1.framerate)

        self.track_client = factory(track_1.bytes[:common_length])
        self.track_operator = factory(track_2.bytes[:common_length])

    def get_silence_info(self):
        mask_client = self.track_client.get_mask(MaskType.SILENCE)
        mask_operator = self.track_operator.get_mask(MaskType.SILENCE)

        mask_both = Mask.intersect(mask_client, mask_operator)

        data = {}
        for name, mask in zip(('client', 'operator', 'both'),
                              (mask_client, mask_operator, mask_both)):
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

    def get_interruptions(self):
        pass



if __name__ == '__main__':

    filename = './audio_samples/Dialog_1/dialog.wav'
    tr_1 = Track.from_file(filename, channel=0)
    tr_2 = Track.from_file(filename, channel=1)
    dialog = Dialog(track_client=tr_1, track_operator=tr_2)

    info = dialog.get_silence_info()
    # pprint.pprint(info)

    result = (
        'Речь оператора, %                             {9:>6.1f}\n'
        'Речь клиента, %                               {10:>6.1f}\n'
        'Речь оператора, сек                           {11:>6.1f}\n'
        'Речь клиента, сек                             {12:>6.1f}\n'
        'Отношение речи оператора к речи клиента       {13:>6.1f}\n'
        'Максимальный участок речи клиента, сек        {14:>6.1f}\n'
        'Максимальный участок речи оператора, сек      {15:>6.1f}\n\n'
        'Общая продолжительность молчания, %:          {0:>6.1f}\n'
        'Общая продолжительность молчания, сек:        {1:>6.1f}\n'
        'Максимальный участок молчания, сек:           {2:>6.1f}\n\n'
        'Продолжительность молчания оператора, %:      {3:>6.1f}\n'
        'Продолжительность молчания оператора, сек:    {4:>6.1f}\n'
        'Максимальный участок молчания оператора, сек: {5:>6.1f}\n\n'
        'Продолжительность молчания клиента, %:        {6:>6.1f}\n'
        'Продолжительность молчания клиента, сек:      {7:>6.1f}\n'
        'Максимальный участок молчания клиента, сек:   {8:>6.1f}\n'
    ).format(
        info['both']['silence_to_total_ratio'] * 100,
        info['both']['silence_duration'],
        info['both']['longest_silence_segment_duration'],
        info['operator']['silence_to_total_ratio'] * 100,
        info['operator']['silence_duration'],
        info['operator']['longest_silence_segment_duration'],
        info['client']['silence_to_total_ratio'] * 100,
        info['client']['silence_duration'],
        info['client']['longest_silence_segment_duration'],
        info['client']  ['speech_to_total_ratio'] * 100,
        info['operator']['speech_to_total_ratio'] * 100,
        info['client']  ['speech_duration'],
        info['operator']['speech_duration'],
        info['operator_to_client_speech_ratio'],
        info['client']  ['longest_speech_segment_duration'],
        info['operator']['longest_speech_segment_duration'],
    )

    print()
    print(result)
