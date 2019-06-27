import socket

from xendbg.gdbserver.protocol import protocol

def serve(host, port, config):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        conn, addr = sock.accept()
        with conn:

            def send_raw(raw):
                conn.sendall(raw)
                print('SEND', raw)

            def recv_raw():
                raw = conn.recv(4096)
                print('RECV', raw)
                return raw

            protocol(send_raw, recv_raw, config)
