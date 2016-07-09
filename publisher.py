#!/usr/bin/env python3
import argparse
import time

from packet import Packet
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall

from common import MCAST_IP, MCAST_ADDR, MCAST_PORT


class Publisher(DatagramProtocol):
    def __init__(self, name, other=None, home_broker=None, receiver=False):
        super().__init__()
        self.name = name
        self.home_broker = home_broker
        self.receiver = receiver
        self._send_loop = None
        self.num = 0
        self.other = other
        self._send_loop = LoopingCall(self._send_numbers)

    def _send_numbers(self):
        time.sleep(0.1)
        p = Packet(self.name, '', self.home_broker, "Message", 'I am {} and I say {}.'.format(self.name, self.num))
        print('(HB={}) I am {} and I say {}.'.format(self.home_broker, self.name, self.num))
        self.transport.write(p.pack(), MCAST_ADDR)
        self.num += 1

    def startProtocol(self):
        self.transport.setTTL(5)
        self.transport.joinGroup(MCAST_IP)
        if not self.receiver:
            self._send_loop.start(interval=1, now=False)

    def datagramReceived(self, datagram, address):
        sender, _, receiver, typ, data = Packet.unpack(datagram)

        if self.receiver and sender != self.name:
            # Home broker change
            if typ == 'HomeBrokerChange':
                self.other.home_broker = data
                print("I, {}, changed home broker to: {}".format(self.name, self.other.home_broker))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Publisher')
    parser.add_argument('name')
    parser.add_argument('home_broker')
    args = parser.parse_args()

    b = Publisher(args.name, home_broker=args.home_broker)
    a = Publisher(args.name, other=b, receiver=True)

    reactor.listenMulticast(MCAST_PORT, a, listenMultiple=True)
    reactor.listenMulticast(MCAST_PORT, b, listenMultiple=True)
    reactor.run()
