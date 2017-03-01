import wave
import functools
import itertools
from enum import IntEnum
import time
import sys

import webrtcvad


def _split(x, n, trim=False):
    print('Building chunks...')
    print('Length:')
    print(len(x))
    print('Memory usage by array:')
    print(sys.getsizeof(x))
    # time.sleep(200)
    chunks = [x[i:i+n] for i in range(0, len(x), n)]
    print('Chunks gotten...')
    if trim and len(chunks[-1]) < n:
        return chunks[:-1]
    return chunks


class Mask:
    def __init__(self, *, mask, frame_duration):
        # mask true when the frame is speech
        self.mask = mask
        self.frame_duration = frame_duration
        self.delta = self.frame_duration / 1000

    def __str__(self):
        return str(self.mask)

    @functools.lru_cache()
    def _count_silence_frames(self):
        return self.mask.count(False)

    def _count_speech_frames(self):
        return len(self.mask) - self._count_silence_frames()

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
        return len([value for value, group in itertools.groupby(self.mask) if value])

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

    @classmethod
    def from_file(cls, filename, channel=None):

        print('Opening file {}'.format(filename))

        with wave.open(filename, 'rb') as container:
            meta = container.getparams()
            bytes_ = container.readframes(meta.nframes)  # Read the whole file

        print('File opened')

        assert meta.nchannels in [1, 2]
        assert meta.comptype == 'NONE'  # No compression

        print('Assertions success.')

        if meta.nchannels == 1:
            binary = bytes_
        else:
            # Dealing with stereo format.
            print('Stereo...')
            assert channel in [0, 1]
            chunks = _split(bytes_, meta.sampwidth)
            print('chunks gotten.')

            assert len(chunks[-1]) == meta.sampwidth
            span = slice(channel, None, 2)  # equvivalent to [0::2] or [1::2]
            binary = b''.join(chunks[span])

        print('binary constructed')

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

        self.common_length = min(len(track_1.bytes), len(track_2.bytes))

        factory = functools.partial(Track,
                                    sampwidth=track_1.sampwidth,
                                    framerate=track_1.framerate)

        self.track_client = factory(track_1.bytes[:self.common_length])
        self.track_operator = factory(track_2.bytes[:self.common_length])

        self.mask_client = self.track_client.get_mask(vad_agressiviness_level, frame_duration)
        self.mask_operator = self.track_operator.get_mask(vad_agressiviness_level, frame_duration)

        self.mask_both = Mask.intersect(self.mask_client, self.mask_operator)
        self.freezingLimit = freezingLimit

    def frames_to_ratio(self, frames_count):
        return self.mask_client.frames_to_ratio(frames_count)

    def frames_to_duration(self, frames_count):
        return self.mask_client.frames_to_duration(frames_count)

    def get_silence_info(self):
        return {
            'operator_speech_ratio' : self.mask_operator.speech_to_total_ratio,
              'client_speech_ratio' : self.mask_client  .speech_to_total_ratio,
            'operator_speech_duration' : self.mask_operator.speech_duration,
              'client_speech_duration' : self.mask_client  .speech_duration,

            'operator_to_client_speech_ratio' : self.mask_operator.speech_duration / self.mask_client.speech_duration,

            'operator_longest_speech_segment_duration' : self.mask_operator.longest_speech_segment_duration,
              'client_longest_speech_segment_duration' : self.mask_client  .longest_speech_segment_duration,

            'operator_silence_ratio' : self.mask_operator.silence_to_total_ratio,
              'client_silence_ratio' : self.mask_client  .silence_to_total_ratio,
                'both_silence_ratio' : self.mask_both    .silence_to_total_ratio,

            'operator_silence_duration' : self.mask_operator.silence_duration,
              'client_silence_duration' : self.mask_client  .silence_duration,
                'both_silence_duration' : self.mask_both    .silence_duration,

            'operator_longest_silence_segment_duration' : self.mask_operator.longest_silence_segment_duration,
              'client_longest_silence_segment_duration' : self.mask_client  .longest_silence_segment_duration,
                'both_longest_silence_segment_duration' : self.mask_both    .longest_silence_segment_duration
        }

    def duration(self):
        return self.track_client.duration

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
        yield (cur, prev, duration)

    def get_influence_array(self):
        return [(i[0], i[2]) for i in self.influence_iterator()]

    def get_interruptions_info(self):
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
            'operator_freezing_duration' : operatorFreezing,
              'client_freezing_duration' : clientFreezing,

            'operator_interruptions_ratio' : self.frames_to_ratio(operatorFrames),
              'client_interruptions_ratio' : self.frames_to_ratio(clientFrames),
                'both_interruptions_ratio' : self.frames_to_ratio(bothFrames),

            'operator_interruptions_duration' : self.frames_to_duration(operatorFrames),
              'client_interruptions_duration' : self.frames_to_duration(clientFrames),
                'both_interruptions_duration' : self.frames_to_duration(bothFrames),

            'operator_interruptions_count' : operator,
              'client_interruptions_count' : client,
                'both_interruptions_count' : both
        }
