import os.path
import logging
import random

from .dialog import Dialog

log = logging.getLogger(__name__)


class Engine:
    def __init__(self, recordings_dir):
        self.recordings_dir = recordings_dir

    def _get_dialog(self, filename, vad_agressiviness_level=3):
        filename = os.path.join(self.recordings_dir, os.path.basename(filename))
        return Dialog(filename, vad_agressiviness_level=vad_agressiviness_level)

    def transcribe_recording(self, filename, **kwargs):
        return self._get_dialog(filename, **kwargs).transcript()

    def process_recording(self, filename, debug=False, **kwargs):
        dialog = self._get_dialog(filename, **kwargs)
        info = dialog.get_silence_info()
        info.update(dialog.get_interruptions_info())

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
