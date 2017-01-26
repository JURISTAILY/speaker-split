import logging
import functools

from transport import Transport

try:
    from basic_pb2 import ConnectionResponse
    from voiceproxy_pb2 import (
        ConnectionRequest, AddData, AddDataResponse, AdvancedASROptions,
    )
except ImportError:
    pass


SSL_PORT = 443

DEFAULT_HOST = 'voice-stream.voicetech.yandex.net'
DEFAULT_PORT = 443
# DEFAULT_PORT = 80
DEFAULT_HOST_OLD = 'asr.yandex.net'
DEFAULT_AUDIO_FORMAT = 'audio/x-pcm;bit=16;rate=16000'
DEFAULT_LANGUAGE = 'ru-RU'

RECOGNITION_MODELS = ['freeform', 'freeform8alaw']
# Use 'freeform8alaw' if your sound comes from a phone call
DEFAULT_RECOGNITION_MODEL = 'freeform'


logger = logging.getLogger(__name__)


class ServerError(RuntimeError):
    pass


class ServerConnection:

    def __init__(self, host, port, key, uuid, ipv4=True):


        self.format = DEFAULT_AUDIO_FORMAT
        self.lang = DEFAULT_LANGUAGE
        self.model = DEFAULT_RECOGNITION_MODEL
        self.punctuation = True


        self.host = host
        self.port = port
        self.ipv4 = ipv4

        self.key = key
        self.uuid = uuid

        self.app = 'local'  # 'KeepAliveClient' ??
        self.service = 'dictation'  # 'asr_dictation' ??

        self.transport_factory = functools.partial(
            Transport, self.host, self.port,
            enable_ssl=(self.port == SSL_PORT),
            ipv4=self.ipv4,
            timeout=0.0,
        )

        self.transport = None
        self.session_id = None
        self._connect()


    def _connect(self):
        self.transport = self.transport_factory()
        self._perform_handshake()
        self.session_id = self._get_session_id()

    def reconnect(self):
        logger.warning('Reconnecting...')
        if self.transport is not None:
            self.transport.close()
        self._connect()


    def _get_session_id(self):
        options = AdvancedASROptions(
            utterance_silence=int(self.inter_utt_silence),
            cmn_latency=self.cmn_latency,
            capitalize=self.capitalize,
            expected_num_count=self.expected_num_count,
            biometry="children",
        )

        request = ConnectionRequest(
            speechkitVersion='',
            serviceName=self.service,
            uuid=self.uuid,
            apiKey=self.key,
            applicationName=self.app,
            device='desktop',
            coords='0, 0',
            topic=self.topic,
            lang=self.lang,
            format=self.format,
            punctuation=self.punctuation,
            advancedASROptions=options,
        )


        chunks,
          callback=None,
          advanced_callback=None,
          callback_module=None,
          format=DEFAULT_FORMAT_VALUE,
          server=DEFAULT_SERVER_VALUE,
          port=DEFAULT_PORT_VALUE,
          key=DEFAULT_KEY_VALUE,
          app='local',
          service='dictation',
          model=DEFAULT_MODEL_VALUE,
          lang=DEFAULT_LANG_VALUE,
          inter_utt_silence=DEFAULT_INTER_UTT_SILENCE,
          cmn_latency=DEFAULT_CMN_LATENCY,
          uuid=DEFAULT_UUID_VALUE,
          reconnect_delay=DEFAULT_RECONNECT_DELAY,
          reconnect_retry_count=DEFAULT_RECONNECT_RETRY_COUNT,
          pending_limit=DEFAULT_PENDING_LIMIT,
          ipv4=False,
          nopunctuation=False,
          realtime=False,
          capitalize=False,
          expected_num_count=0





        self.transport.sendProtobuf(request)
        response = self.transport.recvProtobuf(ConnectionResponse)

        if response.responseCode != 200:
            error_text = 'Wrong response from server, status_code={0}'.format(
                response.responseCode)
            if response.HasField("message"):
                error_text += ', message is "{0}"'.format(response.message)
            raise ServerError(error_text)

        return response.sessionId




    def _perform_handshake(self):

        request = (
            'GET {url} HTTP/1.1\r\n'
            'User-Agent: {user_agent}\r\n'
            'Host: {host}:{port}\r\n'
            'Upgrade: {service}\r\n\r\n'
        ).format(
            user_agent=self.app,
            url='/asr_partial',  # /asr_partial_checked
            host=self.host,
            port=self.port,
            service=self.service,
        ).encode(encoding='ascii')

        self.transport.send(request)

        expected_beginning = b'HTTP/1.1 101 Switching Protocols'
        expected_ending = b'\r\n\r\n'

        response = self.transport.receive_until(expected_ending, critical_length=300)
        if not response.startswith(expected_beginning):
            raise ServerError('Handshake never succeeded. Response: {}'.format(response))

        logger.info('Handshake success.')








