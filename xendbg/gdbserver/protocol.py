import re

from xendbg.gdbserver.handler import handle

ack_re = re.compile(br'\+(?P<rest>.*)')
packet_re = re.compile(br'\$(?P<content>[^#]*)#(?P<checksum>[0-9a-f]{2})(?P<rest>.*)')
# breakin_re = re.compile(br'\x03(?P<rest>.*)')

def checksum(content):
    return '{:02x}'.format(sum(content) % 256).encode('ascii')

def protocol(send_raw, recv_raw, config):
    ack_mode = True
    expecting_ack = True

    def send_packet(content):
        nonlocal ack_mode
        nonlocal expecting_ack
        raw = b'$' + content + b'#' + checksum(content)
        send_raw(raw)
        if ack_mode:
            expecting_ack = True

    def packets():
        nonlocal ack_mode
        nonlocal expecting_ack
        buf = b''
        while True:
            chunk = recv_raw()
            if len(chunk) == 0:
                if len(buf) != 0:
                    raise Exception('connection closed mid-packet:', buf)
                return
            buf += chunk
            if expecting_ack:
                m = ack_re.fullmatch(buf)
                if m is None:
                    raise Exception('was expecting ack:', buf)
                expecting_ack = False
                buf = m['rest']
            m = packet_re.fullmatch(buf)
            if m is not None:
                content = m['content']
                if checksum(content) != m['checksum']:
                    raise Exception('invalid checksum:', buf)
                buf = m['rest']
                # Protocol expects ack after QStartNoAckMode and its response
                if ack_mode:
                    send_raw(b'+')
                if content == b'QStartNoAckMode':
                    send_packet(b'OK')
                    ack_mode = False
                else:
                    yield content

    handle(send_packet, packets(), config)
