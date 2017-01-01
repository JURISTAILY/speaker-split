import socket
import select
import time
import ssl
import pprint
import logging

import utils

CONNECTION_ATTEMPTS = 5
SECONDS_BETWEEN_ATTEMPTS = 1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TransportError(RuntimeError):
    pass


class Transport:

    def __init__(self, host, port, **params):
        for attempts_left in reversed(range(CONNECTION_ATTEMPTS)):
            try:
                self.socket = self._connect(host, port, **params)
                break
            except Exception as ex:
                if not attempts_left:
                    raise
                time.sleep(SECONDS_BETWEEN_ATTEMPTS)

    @staticmethod
    def _connect(host, port, timeout=25, enable_ssl=False, ipv4=False):
        logger.info('Connecting to {host}:{port}...'.format(host=host, port=port))
        if enable_ssl:
            family = socket.AF_INET if ipv4 else socket.AF_INET6
            s = socket.socket(family=family, type=socket.SOCK_STREAM)
            ssl_sock = ssl.wrap_socket(s)
            ssl_sock.connect((host, port))
            logger.debug(repr(ssl_sock.getpeername()))
            logger.debug(ssl_sock.cipher())
            logger.debug(pprint.pformat(ssl_sock.getpeercert()))
            sock = ssl_sock
        else:
            sock = socket.create_connection((host, port), timeout)
            sock.settimeout(timeout)
        return sock

    def __enter__(self):
        return self

    def send(self, data):
        timeout = 0.1
        while True:
            _, wlist, xlist = select.select([], [self.socket], [self.socket], timeout)
            if xlist:
                raise TransportError("send unavailable!")
            if wlist:
                break

        bytes_sent = self.socket.send(data)
        logger.debug('Sent {n} bytes'.format(n=bytes_sent))
        logger.debug(data)

    # def recv(self, length):
    #     # TODO: findout why not working with SSL sockets
    #     # while True:
    #     #     rlist, wlist, xlist = select.select([self.socket], [], [self.socket], 0.1)
    #     #     if len(xlist):
    #     #         raise TransportError("recv unavailable!")
    #     #     if len(rlist):
    #     #         break
    #     return self.socket.recv(length)

    def sendFull(self, message):
        begin = 0
        while begin < len(message):
            begin += self.socket.send(message[begin:])

    def sendMessage(self, message):
        message_length_hex = utils.int_to_hex(len(message))
        self.socket.send(message_length_hex)
        self.socket.send('\r\n')
        self.sendFull(message)
        logger.debug('Message sent. Size: {}'.format(len(message)))

    def _receive_incoming_message_length(self):
        size_info = b''
        while True:
            symbol = self.socket.recv(1)
            if len(symbol) != 1:
                raise TransportError('Received symbol length: {}'.format(len(symbol)))
            if symbol == b'\r':
                # Receiving '\n'.
                self.socket.recv(1)
                break
            size_info += symbol
        return utils.hex_to_int(size_info)

    def _receive_incoming_message(self, size):
        received = b''
        while len(received) < size:
            received += self.socket.recv(size - len(received))
        assert len(received) == size
        return received

    def recvMessage(self):
        length = self._receive_incoming_message_length()
        logger.debug('Got message. Expecting {} bytes.'.format(length))
        return self._receive_incoming_message(length)

    def sendProtobuf(self, protobuf):
        self.sendMessage(protobuf.SerializeToString())

    def recvProtobuf(self, protobufType):
        response = protobufType()
        message = self.recvMessage()
        response.ParseFromString(message)
        return response

    def recvProtobufIfAny(self, protobuf):
        rlist, wlist, xlist = select.select([self.socket], [], [self.socket], 0)
        if rlist:
            return self.recvProtobuf(protobuf)
        return None

    def transfer(self, sendProtobuf, receiveType):
        self.sendProtobuf(sendProtobuf)
        return self.recvProtobuf(receiveType)

    def close(self):
        logger.debug('Closing socket {}...'.format(self.socket))
        self.socket.close()

    def __exit__(self, type, value, traceback):
        self.close()

