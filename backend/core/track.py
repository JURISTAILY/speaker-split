import wave
import json
import subprocess
import os.path
import logging

import webrtcvad

from .mask import Mask

log = logging.getLogger(__name__)

BITS_IN_BYTE = 8
MS_IN_S = 1000
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SPEECHKIT_DIR = os.path.join(BASE_DIR, 'speechkitcloud')
SPEECHKIT_API_KEY = '6478b5d9-bd01-4538-8ff6-87b372205073'
# The only audio format for which ASR works reliably.
SPEECHKIT_AUDIO_FORMAT = 'audio/x-pcm;bit=16;rate=16000'


def _split(binary, n, trim=False):
    assert isinstance(binary, bytes)
    for i in range(0, len(binary), n):
        part = binary[i:i+n]
        if i >= len(binary) - n and trim and len(part) < n:
            pass
        else:
            yield part


class Track:
    def __init__(self, filename):
        with wave.open(filename, 'rb') as container:
            meta = container.getparams()
            binary = container.readframes(meta.nframes)  # Read the whole file

        assert meta.nchannels == 1
        assert meta.framerate in (8000, 16000)
        assert meta.sampwidth == 2  # Only 2 bytes (16 bits) per sample
        assert meta.comptype == 'NONE'  # No compression

        self.meta = meta
        self.bytes = binary
        self.sampwidth = meta.sampwidth
        self.framerate = meta.framerate
        self.filename = filename

    def __len__(self):
        return len(self.bytes)

    def transcript(self):
        assert os.path.isfile(self.filename)

        log.debug('Started transcribing file "{}"'.format(self.filename))

        bit = int(self.sampwidth * BITS_IN_BYTE)
        audio_format = 'audio/x-pcm;bit={};rate={}'.format(bit, self.framerate)

        if audio_format != SPEECHKIT_AUDIO_FORMAT:
            log.warning('Yandex.SpeechKit ASR works reliably only with format "{0}". '
                        'You provided "{1}"'
                        .format(SPEECHKIT_AUDIO_FORMAT, audio_format))

        util = os.path.join(SPEECHKIT_DIR, 'asrclient-cli.py')
        command = [
            util,
            '--key', SPEECHKIT_API_KEY,
            '--format', '"{}"'.format(audio_format),
            '--silent',
            '--model', 'freeform',
            '--callback-module', 'json_callback',
            self.filename,
        ]
        log.debug('Sending command: {}'.format(command))
        output = subprocess.check_output(command, universal_newlines=True)
        return json.loads('[{}]'.format(output))

    @property
    def duration(self):
        """Get track duration in seconds."""
        return (len(self.bytes) / self.sampwidth) / self.framerate

    @property
    def delta(self):
        return 1 / self.framerate

    def _generate_frames(self, frame_duration):
        bytes_per_frame = int(self.sampwidth * self.framerate * frame_duration / MS_IN_S)
        return _split(self.bytes, bytes_per_frame, trim=True)

    def get_mask(self, vad_agressiviness_level, frame_duration=30):
        vad = webrtcvad.Vad(mode=vad_agressiviness_level)
        assert frame_duration in [10, 20, 30]  # ms
        mask = [
            vad.is_speech(frame, self.framerate)
            for frame in self._generate_frames(frame_duration=frame_duration)
        ]
        return Mask(mask=mask, frame_duration=frame_duration)
