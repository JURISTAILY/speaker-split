import os.path
import logging

import pydub

from dialog import Track, Dialog


def mp3_to_wav(f1, f2):
    log = logging.getLogger('pydub.converter')
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())

    mp3 = pydub.AudioSegment.from_file(f1, format='mp3')

    assert mp3.channels == 2
    assert mp3.frame_width == 2
    assert mp3.frame_rate in [8000, 16000]

    mp3.export(f2, format='wav')




class Engine:
    def process_new_recording(self, filename):

        log = logging.getLogger(__name__)

        if filename.endswith('.mp3'):
            log.debug('Dealing with mp3 file.')
            f = os.path.join('/', 'tmp', os.path.basename(filename) + '.wav')
            mp3_to_wav(filename, f)
        else:
            f = filename

        tr_1 = Track.from_file(f, channel=0)
        tr_2 = Track.from_file(f, channel=1)
        dialog = Dialog(track_client=tr_1, track_operator=tr_2)

        info = dialog.get_silence_info()
        info.update(dialog.get_interruptions_info())

        return {
            'duration': dialog.duration(),
            'is_incoming': True,
            'info': info,
            'filename': os.path.basename(filename),
        }


if __name__ == '__main__':

    mp3_to_wav('audio_samples/recording_02-20.mp3',
               'audio_samples/recording_02-20.wav')

