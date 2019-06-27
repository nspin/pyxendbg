from argparse import ArgumentParser

from xendbg.gdbserver.server import server

def main():
    parser = ArgumentParser()
    parser.add_argument('port', type=int)
    parser.add_argument('domain_name')
    args = parser.parse_args()
    config = None
    serve('localhost', port, config)
