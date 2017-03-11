import wave
import os.path

import scipy.io.wavfile


if __name__ == '__main__':

    file_source = os.path.join('audio_samples', 'dialog3.wav')
    file_output = os.path.join('audio_samples', 'dialog1_out.wav')

    rate, data = scipy.io.wavfile.read(file_source)
    print(rate)
    print(data.dtype)
    print(data.shape)

    with wave.open(file_source, 'rb') as source, \
            wave.open(file_output, 'wb') as o:
        params = source.getparams()
        print(params)

        frames = source.readframes(params.nframes)

        print(len(frames))
        print(params.nframes)

        o.setparams(params)
        o.setnchannels(1)

        print(o.getparams())

        def gen(ch):
            window = params.sampwidth * 2
            assert not window % 2
            half = int(window / 2)
            for i in range(0, len(frames), window):
                e = frames[i:i+window]
                yield e[:half] if ch == 'L' else e[half:]

        data = b''.join(gen('L'))

        print(len(data))

        o.writeframes(data)

        print(o.getparams())
