import os.path
import logging
import tempfile
import random
import wave

import pydub

from dialog import Track, Dialog

log = logging.getLogger(__name__)


def gen_temp_file(name=''):
    return tempfile.NamedTemporaryFile(prefix='{}_'.format(name),
                                       suffix='.wav',
                                       delete=False)


def _mp3_to_wav(f1, f2):
    mp3 = pydub.AudioSegment.from_file(f1, format='mp3')

    assert mp3.channels == 2
    assert mp3.sample_width == 2
    assert mp3.frame_rate in [8000, 16000]

    mp3.export(f2, format='wav')


def _stereo_to_two_mono(filename):
    with wave.open(filename, 'rb') as source, \
            gen_temp_file() as temp_l, \
            gen_temp_file() as temp_r, \
            wave.open(temp_l, 'wb') as ch_l, \
            wave.open(temp_r, 'wb') as ch_r:

        params = source.getparams()
        assert params.nchannels == 2

        for ch in (ch_l, ch_r):
            ch.setparams(params)
            ch.setnchannels(1)

        frames = source.readframes(params.nframes)

        def gen(ch):
            window = params.sampwidth * 2
            half = int(window / 2)
            for i in range(0, len(frames), window):
                e = frames[i:i+window]
                yield e[:half] if ch == 'L' else e[half:]

        data_l = b''.join(gen('L'))
        data_r = b''.join(gen('R'))
        ch_l.writeframes(data_l)
        ch_r.writeframes(data_r)

        return temp_l.name, temp_r.name


class Engine:

    def __init__(self, recordings_dir):
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
    print(_stereo_to_two_mono('audio_samples/dialog1.wav'))
