import wave
import functools
import itertools
# from collections.abc import Sequence

import numpy as np

try:
    import webrtcvad
except ImportError:
    webrtcvad = None


class VoiceMask:
    def __init__(self, *, mask, delta):
        self.mask = mask
        self.delta = delta

    # def __iter__(self):
    #     return iter(self.mask)

    @functools.lru_cache()
    def silent_samples_count(self):
        return len([True for x in self.mask if not x])

    def silence_duration_total(self):
        return self.silent_samples_count() * self.delta

    def silence_duration_total_ratio(self):
        return self.silent_samples_count() / len(self.mask)

    def silence_duration_max(self):
        count = max([len(list(iterator))
                    for value, iterator in itertools.groupby(self.mask) if not value])
        return count * self.delta

    @staticmethod
    def intersect(first, second, *, voices=True):
        assert first.delta == second.delta
        assert len(first.mask) == len(second.mask)

        def sect(a, b):
            return (a and b) if voices else (a or b)

        return VoiceMask(mask=[sect(a, b) for a, b in zip(first, second)],
                         delta=first.delta)


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
        return (self.bytes / self.sampwidth) / self.framerate


    def _get_frames(self, frame_duration):
        # frame_duration is in [ms].

        bytes_per_frame = int(
            self.sampwidth * self.framerate * frame_duration / 1000
        )

        def _split(x, n):
            return [x[i:i+n] for i in range(0, len(x), n)]

        return _split(self.bytes, bytes_per_frame)[:-1]


    def get_voicemask(self, frame_duration=30):
        assert frame_duration in [10, 20, 30]

        aggressiveness_level = 3  # 0, 1, 2, 3
        vad = webrtcvad.Vad(mode=aggressiveness_level)

        frames = self._get_frames(frame_duration=frame_duration)
        mask = [vad.is_speech(frame, self.framerate) for frame in frames]

        return VoiceMask(mask=mask, delta=frame_duration/1000)


    @property
    def delta(self):
        return 1 / self.framerate

    @classmethod
    def from_file(cls, filename):

        with wave.open(filename, 'rb') as container:
            meta = container.getparams()
            bytes = container.readframes(meta.nframes)  # Read the whole file

        assert meta.nchannels == 1  # Only mono
        return cls(bytes, sampwidth=meta.sampwidth, framerate=meta.framerate)

    def is_same_format(self, other):
        return (self.framerate, self.sampwidth) == (other.framerate, other.sampwidth)

    def get_silence_info(self):
        info = {
            'silence_duration_total': 0.0,
            'silence_duration_max': 0.0,
            'silence_duration_average': 0.0,
            'silence_duration_total_percent': 0.0,
        }
        return info


class Dialog:

    def __init__(self, file_1, file_2):

        track_1 = Track.from_file(file_1)
        track_2 = Track.from_file(file_2)

        assert track_1.is_same_format(track_2)

        common_length = min(len(track_1.bytes), len(track_2.bytes))

        factory = functools.partial(Track,
                                    sampwidth=track_1.sampwidth,
                                    framerate=track_1.framerate)

        self.track_client   = factory(track_1.bytes[:common_length])
        self.track_operator = factory(track_2.bytes[:common_length])

    def get_silence_info(self):
        mask_client = self.track_client.get_voicemask()
        mask_operator = self.track_operator.get_voicemask()

        common_mask = VoiceMask.intersect(mask_client, mask_operator)


        return {
            'client_silence_duration_total': 0.0,
            'client_silence_duration_total': 0.0,
            'client_silence_duration_total': 0.0,
            'client_silence_duration_total': 0.0,
            'client_silence_duration_total': 0.0,
            'client_silence_duration_total': 0.0,
            'client_silence_duration_total': 0.0,
            'client_silence_duration_total': 0.0,
            'client_silence_duration_total': 0.0,
            'client_silence_duration_total': 0.0,
            'client_silence_duration_total': 0.0,
            'client_silence_duration_total': 0.0,
        }



if __name__ == '__main__':
    track = Track.from_file('./audio_samples/sample.wav')
    mask = track.get_voicemask()
    print(mask.silence_duration_max())
