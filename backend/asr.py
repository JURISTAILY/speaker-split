import time
from enum import Enum
import wave

import requests

API_KEY = 'd0f636aa-b10a-495d-ae5a-c56459497c1c'
UUID = '028f39b0c6a811e69d9dcec0c932ce01'
HOST = 'asr.yandex.net'
URL = 'https://{host}/asr_xml'.format(host=HOST)
TOPICS = 'notes queries maps dates names numbers music buying'.split()
CONTENT_TYPES = [
    'audio/x-wav',
    'audio/x-mpeg-3',
    'audio/x-speex',
    'audio/ogg;codecs=opus',
    'audio/webm;codecs=opus',
    'audio/x-mpeg-3',
    'audio/x-pcm;bit=16;rate=16000',
    'audio/x-pcm;bit=16;rate=8000',
    'audio/x-alaw;bit=13;rate=8000',
]

Method = Enum('Method', 'POST CHUNKED STREAM')


def _prepare_pcm(filename, out_):
    with wave.open(filename, 'rb') as obj:
        params = obj.getparams()
        binary = obj.readframes(params.nframes)
    with open(out_, 'wb') as o:
        o.write(binary)


def _prepare_chunks(in_, out_, size=200):

    def w(f, s):
        if isinstance(s, bytes):
            f.write(s)
        else:
            f.write(s.encode('ascii'))
            # f.write(bytes(s, encoding='ascii'))

    chunked_size = size

    def __len__(self):
        return self.oldrt.getSize()

    with open(out_, 'wb') as o:
        with open(in_, 'rb') as i:
            content = i.read()
        while len(content) > 0:
            size = min(len(content), chunked_size)
            w(o, hex(size)[2:])
            w(o, '\r\n')
            w(o, content[:size])
            w(o, '\r\n')
            content = content[size:]
        w(o, '0\r\n\r\n')


class Manager:
    def __init__(self, method, topic='notes'):
        assert topic in TOPICS
        self.method = method
        self.topic = topic
        self.url_params = {
            'uuid': UUID,
            'key': API_KEY,
            'topic': self.topic,
            'lang': 'ru-RU',
        }

    def recognize_chunked(self, filename):
        masks = ['{name}', '{name}.pcm', '{name}.pcm.chunked']
        names = [n.format(name=filename) for n in masks]
        _prepare_pcm(names[0], names[1])
        _prepare_chunks(names[1], names[2])

        with open(names[2], 'rb') as f:
            binary = f.read()

        headers = {
            'Content-Type': 'audio/x-pcm;bit=16;rate=8000',
            'Host': HOST,
            'Transfer-Encoding': 'chunked',
        }

        response = requests.post(
            URL, data=binary, params=self.url_params, headers=headers)

        return response.text

    def recognize_post(self, filename):
        with open(filename, 'rb') as f:
            binary = f.read()

        headers = {
            'Content-Type': 'audio/x-wav',
            'Host': HOST,
        }

        response = requests.post(
            URL, data=binary, params=self.url_params, headers=headers)

        return response.text

    def recognize(self, filename):
        if self.method is Method.POST:
            return self.recognize_post(filename)
        elif self.method is Method.CHUNKED:
            return self.recognize_chunked(filename)
        raise NotImplementedError


if __name__ == '__main__':

    manager = Manager(Method.CHUNKED)

    s = time.time()
    data = manager.recognize('./wilstream_long.wav')
    print(data)
    f = time.time() - s
    print(f)
