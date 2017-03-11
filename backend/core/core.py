import os.path
import logging
import random
import tempfile

from .dialog import Track, Dialog
from .utils import get_wav_file

log = logging.getLogger(__name__)


class Engine:

    def __init__(self, recordings_dir):
        self.recordings_dir = recordings_dir

    def transcribe_recording(self, filename, *, vad_agressiviness_level=3):
        """
            After calling this function all
            created temporary files are deleted automatically.
        """
        filename = os.path.join(self.recordings_dir, os.path.basename(filename))

        temp_dir = tempfile.TemporaryDirectory
        wav_file = get_wav_file(filename, temp_dir=temp_dir)
        dialog = Dialog.from_file(wav_file,
                                  vad_agressiviness_level=vad_agressiviness_level,
                                  temp_dir=temp_dir)
        return dialog.transcript()

    def process_recording(self, filename, debug=False, *, vad_agressiviness_level=3):
        temp_dir = tempfile.TemporaryDirectory
        filename = os.path.join(self.recordings_dir, os.path.basename(filename))
        wav_file = get_wav_file(filename, temp_dir=temp_dir)

        tr_1 = Track.from_file(wav_file, channel=0)
        tr_2 = Track.from_file(wav_file, channel=1)

        dialog = Dialog(track_client=tr_1, track_operator=tr_2,
                        vad_agressiviness_level=vad_agressiviness_level)

        info = dialog.get_silence_info()
        info.update(dialog.get_interruptions_info())

        log.debug('Data from wav-file extracted.')

        data = {
            'duration': dialog.duration(),
            'is_incoming': random.choice([True, False]),
            'info': info,
            'filename': os.path.basename(filename),
        }

        if debug:
            data.update({
                'debug': {
                    'interruptions': dialog.get_influence_array(),
                    'client_raw_mask': dialog.mask_client.raw_mask,
                    'operator_raw_mask': dialog.mask_operator.raw_mask,
                    'client_mask': dialog.mask_client.mask,
                    'operator_mask': dialog.mask_operator.mask,
                },
            })

        return data
