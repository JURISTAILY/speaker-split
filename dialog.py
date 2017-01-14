import wave
import functools
import itertools
from enum import Enum
# from collections.abc import Sequence

import numpy as np

try:
    import webrtcvad
except ImportError:
    webrtcvad = None

VAD_AGRESSIVINESS_LEVEL = 3  # 0, 1, 2, 3

MaskType = Enum('MaskType', 'SPEECH, SILENCE')


class Mask:
    def __init__(self, *, mask, frame_duration):
        self.mask = mask
        self.frame_duration = frame_duration
        self.delta = self.frame_duration / 1000

    def __str__(self):
        return str(self.mask)

    @functools.lru_cache()
    def _count_events(self):
        return self.mask.count(True)

    @property
    def total_duration(self):
        return self._count_events() * self.delta

    @property
    def total_ratio(self):
        return self._count_events() / len(self.mask)

    @property
    def longest_segment_duration(self):
        count = max(
            len(list(group)) for value, group in itertools.groupby(self.mask) if value
        )
        return count * self.delta

    @property
    def segments_amount(self):
        return len([_ for value, group in itertools.groupby(self.mask) if value])

    @classmethod
    def intersect(cls, first, second):
        assert first.frame_duration == second.frame_duration
        assert len(first.mask) == len(second.mask)

        return cls(mask=[a and b for a, b in zip(first, second)],
                   frame_duration=first.frame_duration)


class Track:

    def __init__(self, bytes, *, sampwidth, framerate):
        self.bytes = bytes
        self.sampwidth = sampwidth
        self.framerate = framerate

        assert self.sampwidth == 2  # only 2 bytes (16 bits) per sample
        assert self.framerate in [8000, 16000]

        self.signal = np.fromstring(self.bytes, dtype=np.int16)

    @property
    def duration(self):
        """Get track duration in seconds."""
        return (len(self.bytes) / self.sampwidth) / self.framerate

    def _get_frames(self, frame_duration):
        # frame_duration is in [ms].

        bytes_per_frame = int(
            self.sampwidth * self.framerate * frame_duration / 1000
        )

        def _split(x, n):
            return [x[i:i+n] for i in range(0, len(x), n)]

        return _split(self.bytes, bytes_per_frame)[:-1]

    def get_mask(self, mask_type, frame_duration=30):
        """Frame duration is in ms."""
        assert frame_duration in [10, 20, 30]
        vad = webrtcvad.Vad(mode=VAD_AGRESSIVINESS_LEVEL)
        frames = self._get_frames(frame_duration=frame_duration)

        def crit(frame):
            is_speech = vad.is_speech(frame, self.framerate)
            return is_speech is (mask_type is MaskType.SPEECH)

        return Mask(mask=[crit(frame) for frame in frames],
                    frame_duration=frame_duration)

    @property
    def delta(self):
        return 1 / self.framerate

    @classmethod
    def from_file(cls, filename):

        with wave.open(filename, 'rb') as container:
            meta = container.getparams()
            bytes = container.readframes(meta.nframes)  # Read the whole file

        assert meta.nchannels == 1  # Only mono
        assert meta.comptype == 'NONE'  # No compression
        return cls(bytes, sampwidth=meta.sampwidth, framerate=meta.framerate)

    @classmethod
    def same_format(cls, first, second):
        return (first.framerate, first.sampwidth) == (other.framerate, other.sampwidth)


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

    def get_silence_info(self, mask_type):
        mask_client = self.track_client.get_mask(MaskType.SILENCE)
        mask_operator = self.track_operator.get_mask(MaskType.SILENCE)

        mask_both = Mask.intersect(mask_client, mask_operator)

        data = {}
        for name, mask in zip(('client', 'operator', 'both'),
                              (mask_client, mask_operator, mask_both)):
            data[name] = {
                'total_duration': mask.total_duration,
                'total_ratio': mask.total_ratio,
                'longest_segment_duration': mask.longest_segment_duration,
                'segments_amount': mask.segments_amount,
            }

        return data



if __name__ == '__main__':

    tr_1 = Track.from_file('./audio_samples/Dialog_1/file_1.wav')
    tr_2 = Track.from_file('./audio_samples/Dialog_1/file_2.wav')
    dialog = Dialog(tr_1, tr_2)
    print(dialog.get_silence_info())
