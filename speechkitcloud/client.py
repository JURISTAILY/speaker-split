import logging
import functools

from transport import Transport

from basic_pb2 import ConnectionResponse
from voiceproxy_pb2 import (
    ConnectionRequest, AddData, AddDataResponse, AdvancedASROptions,
)


SSL_PORT = 443

logger = logging.getLogger(__name__)


class ServerError(RuntimeError):
    pass


class ServerConnection:

    def __init__(self, host, port, key, uuid, ipv4=False):

        self.host = host
        self.port = port
        self.ipv4 = ipv4

        self.key = key
        self.uuid = uuid

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
        self.session_id = self._get_session_id()

    def reconnect(self):
        logger.warning('Reconnecting...')
        if self.transport is not None:
            self.transport.close()
        self._connect()


    def _get_session_id(self):

        self._perform_handshake()

        response = self._send_init_request()
        if response.responseCode != 200:
            error_text = 'Wrong response from server, status_code={0}'.format(
                response.responseCode)
            if response.HasField("message"):
                error_text += ', message is "{0}"'.format(response.message)
            raise ServerError(error_text)

        return response.sessionId




    def _perform_handshake(self):

        request = (
            'GET /asr_partial_checked HTTP/1.1\r\n'
            'User-Agent: {user_agent}\r\n'
            'Host: {host}:{port}\r\n'
            'Upgrade: {service}\r\n\r\n'
        ).format(
            user_agent=self.app,
            host=self.host,
            port=self.port,
            service=self.service,
        ).encode(encoding='ascii')

        self.transport.send(request)
        check = b'HTTP/1.1 101 Switching Protocols'

        CRITICAL_LENGTH = 10 * len(check)

        buff = b''
        while True:
            buff += self.transport.recv(1)
            if buff.startswith(check) and buff.endswith(b'\r\n\r\n'):
                break
            if len(buff) > CRITICAL_LENGTH:
                raise ServerError('Handshake never succeeded: {}'.format(buff))

        logger.info('Handshake success.')




    def _send_init_request(self):

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

        self.transport.sendProtobuf(request)
        return self.transport.recvProtobuf(ConnectionResponse)






