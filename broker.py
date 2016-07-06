#!/usr/bin/env python3
import socketserver
import sys


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
        print('{}:{} connected'.format(*self.client_address))

    def handle(self):
        client_host, client_port = self.client_address
        other_brokers = self.server.other_brokers

        while True:
            data = self.rfile.readline()
            data = data.decode().tstrip('\n')
            print("{}:{} wrote: {}".format(client_host, client_port, data))

    def finish(self):
        print("{}:{} closed the connection :(".format(*self.client_address), file=sys.stderr)

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
