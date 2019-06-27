from collections import namedtuple
import binascii

Config = namedtuple('Config', ['domain'])

triple = b'x86_64-unknown-linux-gnu'

def init_state(self, config):
    self.domain = config.domain

def add_routes(send, route):

    def ok():
        send(b'OK')

    def send_assocs(d):
        send(b':'.join(
            k.encode('ascii') + b':' + (v if type(v) is bytes else v.encode('ascii'))
            for k, v in d.items()
            ))

    def send_list(l):
        send(b':'.join(
            (v if type(v) is bytes else v.encode('ascii'))
            for v in l
            ))

    @route(b'QEnableErrorStrings')
    def f(self):
        ok()
  
    @route(b'QThreadSuffixSupported')
    def f(self):
        ok()

    @route(b'QListThreadsInStopReply')
    def f(self):
        ok()

    @route(b'qHostInfo')
    def f(self):
        send_assocs({
            'triple': binascii.hexlify(triple),
            'ptrsize': str(self.domain.get_word_size()),
            'endian': 'little',
            'hostname': binascii.hexlify(self.domain.get_name()),
            })

    @route(b'qProcessInfo')
    def f(self):
        pid = 1
        send_assocs({
            'pid': str(pid),
            'ptrsize': str(self.domain.get_word_size()),
            'endian': 'little',
            })

    @route(b'qC')
    def f(self):
        send(b'')

    @route(b'qfThreadInfo')
    def f(self):
        send(b'')

    @route(b'qsThreadInfo')
    def f(self):
        send(b'')

    @route(b'qWatchpointSupportInfo:?')
    def f(self):
        send(b'')

    @route(b'qSupported(:(?P<features>.*?))?')
    def f(self, features):
        send_list((
            'PacketSize=20000',
            'QStartNoAckMode+',
            'QThreadSuffixSupported+',
            'QListThreadsInStopReplySupported+',
            ))

    @route(b'qRegisterInfo.*') # ?
    def f(self):
        send(b'')

    @route(b'qMemoryRegionInfo.*') # ?
    def f(self):
        send(b'')
