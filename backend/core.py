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

def wav_input(to_decorate):
    def decorated(self, filename, is_incoming = True) :
        if filename.endswith('.mp3'):
            self.log.debug(
                'Dealing with mp3 file ({}).'
                .format(os.path.basename(filename))
            )
            wav_file = os.path.join(
                tempfile.gettempdir(),
                '.{}.temp.wav'.format(os.path.basename(filename)),
            )
            _mp3_to_wav(filename, wav_file)
            self.log.debug('mp3 file converted to temporary wav-file "{}".'.format(wav_file))
            result = to_decorate(self, filename, wav_file, is_incoming)
            os.remove(wav_file)
            self.log.debug('Temporary file "{}" deleted.'.format(wav_file))
            return result
        else:
            return to_decorate(self, filename, filename, is_incoming)
    return decorated

class Engine:
    def __init__(self):
        self.log = logging.getLogger(__name__)


    @wav_input
    def process_recording(self, filename, wav_file, is_incoming):

        tr_1 = Track.from_file(wav_file, channel=0)
        tr_2 = Track.from_file(wav_file, channel=1)
        dialog = Dialog(track_client=tr_1, track_operator=tr_2)

        info = dialog.get_silence_info()
        info.update(dialog.get_interruptions_info())

        self.log.debug('Data from wav-file extracted.')

        return {
            'duration': dialog.duration(),
            'is_incoming': is_incoming,
            'info': info,
            'filename': os.path.basename(filename),
        }

    @wav_input
    def process_recording_with_debug(self, filename, wav_file, is_incoming):

        tr_1 = Track.from_file(wav_file, channel=0)
        tr_2 = Track.from_file(wav_file, channel=1)
        dialog = Dialog(track_client=tr_1, track_operator=tr_2)

        result = self.process_recording(filename, is_incoming)
        result.update({'debug' : {
            'interruptions' : dialog.get_influence_array(),
            'client_mask' : dialog.mask_client.mask,
            'operator_mask' : dialog.mask_operator.mask
            }})
        return result
