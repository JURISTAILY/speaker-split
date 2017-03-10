import os.path
import logging
import random
import wave

import pydub

from dialog import Track, Dialog
from settings import RECORDINGS_DIR

log = logging.getLogger(__name__)


def _mp3_to_wav(f1, f2):
    mp3 = pydub.AudioSegment.from_file(f1, format='mp3')

    assert mp3.channels == 2
    assert mp3.sample_width == 2
    assert mp3.frame_rate in [8000, 16000]

    mp3.export(f2, format='wav')


class Engine:

    def __init__(self, recordings_dir=RECORDINGS_DIR):
        self.recordings_dir = recordings_dir

    @staticmethod
    def _get_wav_file(filename):
        basename = os.path.basename(filename)

        if basename.endswith('.wav'):
            return filename

        if basename.endswith('.mp3'):
            with gen_temp_file(basename) as temp:
                wav_file = temp.name

            _mp3_to_wav(filename, wav_file)
            log.warning('mp3 file converted to temporary wav-file: "{}". '
                        'It is not deleted.'.format(wav_file))
            return wav_file

        raise RuntimeError('Unsupported file format: {}'.format(basename))

    def transcribe_recordig(self, filename, *, vad_agressiviness_level=3):

        filename = os.path.join(self.recordings_dir, os.path.basename(filename))
        wav_file = self._get_wav_file(filename)

        dialog = Dialog.from_file(wav_file, vad_agressiviness_level=vad_agressiviness_level)
        return dialog.transcript()

    def process_recording(self, filename, debug=False, *, vad_agressiviness_level=3):

        filename = os.path.join(self.recordings_dir, os.path.basename(filename))
        wav_file = self._get_wav_file(filename)

        print('Init tracks...')

        tr_1 = Track.from_file(wav_file, channel=0)
        tr_2 = Track.from_file(wav_file, channel=1)
        print('Tracks constructed')
        dialog = Dialog(track_client=tr_1, track_operator=tr_2,
                        vad_agressiviness_level=vad_agressiviness_level)

        print('Dialog constructed.')

        info = dialog.get_silence_info()

        print('Silence info gotten.')
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

if __name__ == '__main__':
    engine = Engine()
    print(engine.transcribe_recordig("dialog2.wav"))
