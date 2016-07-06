#!/usr/bin/env python3
import socketserver
import sys

import struct


class BrokerTCPServer(socketserver.TCPServer):
    """
    Broker (TCP server) that additionally takes a list of other brokers than himself.
    """
    def __init__(self, server_address, RequestHandlerClass, other_brokers, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.other_brokers = other_brokers


class BrokerHandler(socketserver.StreamRequestHandler):
    """
    Handler for the broker.
    """

    def setup(self):
        print('{}:{} -> Connected'.format(*self.client_address), file=sys.stderr)

    def handle(self):
        client_host, client_port = self.client_address
        other_brokers = self.server.other_brokers

        while True:
            raw_msg_length = self.request.recv(4)
            if not raw_msg_length:
                break

            msg_length = struct.unpack('>I', raw_msg_length)[0]
            msg = self.request.recv(msg_length)
            line = msg.decode()

            print("{}:{} -> {}".format(client_host, client_port, line))

    def finish(self):
        print("{}:{} -> Closed the connection :(".format(*self.client_address), file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} (<host>:<port>) (<o_host>:<o_port>) [(<o_host>:<o_port>) ...] '.format(
            __file__), file=sys.stderr)
        sys.exit(3)

    host, port = sys.argv[1].split(':')
    port = int(port)
    other_brokers = [(h, p) for h, p in map(lambda s: s.split(':'), sys.argv[2:])]

    server = BrokerTCPServer((host, port), BrokerHandler, other_brokers)

    print("Starting broker on {}:{} ...".format(host, port))
    server.serve_forever()
