import wave
from collections import namedtuple
import time
import json

import numpy as np
import matplotlib.pyplot as plt

import webrtcvad

try:
    from python_speech_features import mfcc
except ImportError:
    mfcc = None


def _get_amplitudes(signal):
    return np.absolute(np.fft.fft(signal))


def _normalize(signal):
    scale = np.absolute(signal).max()
    return (1/scale) * signal


def _filter(signal):
    return _normalize(signal)


Meta = namedtuple('Meta', 'sampwidth, framerate')






class Audio:

    def __init__(self, bytes, sampwidth, framerate):
        self.bytes = bytes
        self.sampwidth = sampwidth
        self.framerate = framerate

        assert self.sampwidth == 2  # only 2 bytes (16 bits) per sample
        assert self.framerate in [8000, 16000]

        self.signal = np.fromstring(self.bytes, dtype=np.int16)

    @property
    def duration(self):
        return (self.bytes / self.sampwidth) / self.framerate

    @classmethod
    def from_file(cls, filename):

        with wave.open(filename, 'rb') as container:
            meta = container.getparams()
            bytes = container.readframes(-1)  # Read the whole stream

        assert meta.nchannels == 1  # only mono
        return cls(bytes, sampwidth=meta.sampwidth, framerate=meta.framerate)

    def is_compatible_with(self, other):
        return self.meta.framerate == other.meta.framerate

    def _get_frames(self, frame_duration):
        # frame_duration is in [ms].

        bytes_per_frame = int(
            self.meta.sampwidth * self.meta.framerate * frame_duration / 1000
        )
        
        def _split(x, n):
            return [x[i:i+n] for i in range(0, len(x), n)]

        return _split(self.bytes, bytes_per_frame)[:-1]

    def _perform_vad(self, frame_duration=30):
        assert frame_duration in [10, 20, 30]  # requirement of vad.is_speech
        frames = self._get_frames(frame_duration=frame_duration)
        aggressiveness_level = 3  # 0, 1, 2, 3
        vad = webrtcvad.Vad(mode=aggressiveness_level)
        Result = namedtuple('Result', 'timestamp, is_speech')
        return [Result(timestamp=n*frame_duration/1000,
                       is_speech=vad.is_speech(frame, self.meta.framerate))
                for n, frame in enumerate(frames)]

    def _get_mfcc_features(self, frame_duration=10):
        # Defaults: winlen=0.025, winstep=0.01
        return mfcc(self.signal, samplerate=self.meta.framerate,
                    winstep=frame_duration/1000)

    def build_features(self):
        frame_duration = 10  # ms

        features = self._get_mfcc_features(frame_duration=frame_duration)
        vad = [v.is_speech for v in self._perform_vad(frame_duration=frame_duration)]

        common_len = min(len(features), len(vad))
        features = features[:common_len]
        vad = vad[:common_len]

        time_ = np.linspace(0, self.duration, num=common_len)

        def build(t, v, f):
            return dict(timestamp=t, is_speech=v,
                        features=f.tolist())

        return [build(t, v, f) for t, v, f in zip(time_, vad, features)]




def do():
    audio = Audio('sample.wav')
    features = audio.build_features()
    with open('data.json', 'w') as outfile:
        json.dump(features, outfile, sort_keys=True, indent=4)



if __name__ == '__main__':

    do()
