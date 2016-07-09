#!/usr/bin/env python3
import argparse

from packet import Packet
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol

from common import MCAST_IP, MCAST_PORT

hashes = []


class Subscriber(DatagramProtocol):
    def __init__(self, home_broker):
        super().__init__()
        self.home_broker = home_broker

    def startProtocol(self):
        self.transport.setTTL(5)
        self.transport.joinGroup(MCAST_IP)

    def datagramReceived(self, datagram, address):
        sender, broker, receiver, typ, data = Packet.unpack(datagram)
        h = hash(str([sender, broker, receiver, typ, data]))

        if typ == "Message" and broker == self.home_broker and h not in hashes:
            print("<{}> (HB: {}): {}".format(sender, self.home_broker, data))
            hashes.append(h)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Broker')
    parser.add_argument('home_broker')
    args = parser.parse_args()

    reactor.listenMulticast(MCAST_PORT, Subscriber(args.home_broker), listenMultiple=True)
    reactor.run()
