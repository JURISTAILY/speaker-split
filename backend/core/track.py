import wave
import json
import subprocess
import os.path
import logging

import webrtcvad

from .mask import Mask

log = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SPEECHKIT_DIR = os.path.join(BASE_DIR, 'speechkitcloud')
SPEECHKIT_API_KEY = '6478b5d9-bd01-4538-8ff6-87b372205073'


def _split(x, n, trim=False):
    # TODO: Refactor this shit. It eats memory like a pig.
    chunks = [x[i:i+n] for i in range(0, len(x), n)]
    if trim and len(chunks[-1]) < n:
        return chunks[:-1]
    return chunks


class Track:
    def __init__(self, bytes_, *, sampwidth, framerate, filename):
        self.bytes = bytes_
        self.sampwidth = sampwidth
        self.framerate = framerate
        self.filename = filename

        assert self.sampwidth == 2  # only 2 bytes (16 bits) per sample
        assert self.framerate in [8000, 16000]

    def __len__(self):
        return len(self.bytes)

    def transcript(self):
        print("transcribe filename {}".format(self.filename))
        assert os.path.isfile(self.filename)
        util = os.path.join(SPEECHKIT_DIR, 'asrclient-cli.py')
        bits = int(self.sampwidth * 8)
        command = [
            util,
            '--key={}'.format(SPEECHKIT_API_KEY),
            '--format="audio/x-pcm;bit={};rate={}"'.format(bits, self.framerate),
            '--silent',
            '--format="audio/x-pcm;bit=16;rate={}"'.format(self.framerate),
            '--callback-module', 'json_callback',
            self.filename,
        ]
        log.warning('Sending command: {}'.format(command))
        output = subprocess.check_output(command, universal_newlines=True)
        return json.loads('[{}]'.format(output))

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

        return cls(binary, sampwidth=meta.sampwidth,
                   framerate=meta.framerate, filename=filename)

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
