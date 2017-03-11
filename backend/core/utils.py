import tempfile
import wave
import os.path
import logging

import pydub

log = logging.getLogger(__name__)


def _gen_temp_file(temp_dir=None):
    return tempfile.NamedTemporaryFile(prefix='speech_temp_',
                                       suffix='.wav',
                                       dir=temp_dir,
                                       delete=False,
                                       )


def stereo_to_two_mono(filename, temp_dir=None):
    with wave.open(filename, 'rb') as source, \
            _gen_temp_file(temp_dir) as temp_l, \
            _gen_temp_file(temp_dir) as temp_r, \
            wave.open(temp_l, 'wb') as ch_l, \
            wave.open(temp_r, 'wb') as ch_r:
        params = source.getparams()
        assert params.nchannels == 2
        frames = source.readframes(params.nframes)
        # That is an invariant. Must always be True.
        assert params.nframes == len(frames) // (params.sampwidth * params.nchannels)

        for ch in (ch_l, ch_r):
            ch.setparams(params)
            ch.setnchannels(1)

        def gen(ch):
            window = params.sampwidth * 2
            assert not window % 2
            half = int(window / 2)
            for i in range(0, len(frames), window):
                e = frames[i:i+window]
                yield e[:half] if ch == 'L' else e[half:]

        data_l = b''.join(gen('L'))
        data_r = b''.join(gen('R'))
        ch_l.writeframes(data_l)
        ch_r.writeframes(data_r)

        return temp_l.name, temp_r.name


def _mp3_to_wav(f1, f2):
    mp3 = pydub.AudioSegment.from_file(f1, format='mp3')

    assert mp3.channels == 2
    assert mp3.sample_width == 2
    assert mp3.frame_rate in [8000, 16000]

    mp3.export(f2, format='wav')


def get_wav_file(filename, *, temp_dir=None):
    assert temp_dir is not None
    basename = os.path.basename(filename)

    if basename.endswith('.wav'):
        return filename

    if basename.endswith('.mp3'):
        with _gen_temp_file(temp_dir) as temp:
            wav_file = temp.name

        _mp3_to_wav(filename, wav_file)
        log.warning('mp3 file converted to temporary wav-file: "{}". '
                    'It is not deleted.'.format(wav_file))
        return wav_file

    raise RuntimeError('Unsupported file format: {}'.format(basename))
