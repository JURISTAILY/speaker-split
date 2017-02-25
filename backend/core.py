import os.path
import os
import logging
import tempfile

import pydub

from dialog import Track, Dialog


def _mp3_to_wav(f1, f2):
    mp3 = pydub.AudioSegment.from_file(f1, format='mp3')

    assert mp3.channels == 2
    assert mp3.sample_width == 2
    assert mp3.frame_rate in [8000, 16000]

    mp3.export(f2, format='wav')


class Engine:
    def process_new_recording(self, filename):
        temporary = False
        log = logging.getLogger(__name__)

        if filename.endswith('.mp3'):
            log.debug(
                'Dealing with mp3 file ({}).'
                .format(os.path.basename(filename))
            )
            wav_file = os.path.join(
                tempfile.gettempdir(),
                '.{}.temp.wav'.format(os.path.basename(filename)),
            )
            _mp3_to_wav(filename, wav_file)
            temporary = True
            log.debug('mp3 file converted to temporary wav-file "{}".'.format(wav_file))
        else:
            wav_file = filename

        tr_1 = Track.from_file(wav_file, channel=0)
        tr_2 = Track.from_file(wav_file, channel=1)
        dialog = Dialog(track_client=tr_1, track_operator=tr_2)

        info = dialog.get_silence_info()
        info.update(dialog.get_interruptions_info())

        log.debug('Data from wav-file extracted.')

        if temporary:
            os.remove(wav_file)
            log.debug('Temporary file "{}" deleted.'.format(wav_file))

        return {
            'duration': dialog.duration(),
            'is_incoming': True,
            'info': info,
            'filename': os.path.basename(filename),
        }
