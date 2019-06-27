import re
import inspect

from xendbg.gdbserver.routes import init_state, add_routes

def handle(send_packet, packets, config):

    routes = []

    def add_route(pattern):
        def consume(handler_fn):
            routes.append((re.compile(pattern), handler_fn))
        return consume

    add_routes(send_packet, add_route)

    class HandlerState:
        __init__ = init_state

    handler_state = HandlerState(config)

    for packet in packets:
        for r, handler_fn in routes:
            m = r.fullmatch(packet)
            if m is not None:
                argspec = inspect.getargspec(handler_fn)
                assert argspec.args[0] == 'self'
                args = (m[arg] for arg in argspec.args[1:])
                handler_fn(handler_state, *args)
                break
        else:
            print('packet fell through:', packet)
            send_packet(b'')
