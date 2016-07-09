#!/usr/bin/env python3
import argparse
import random

from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall

from common import MCAST_IP, MCAST_PORT, MCAST_ADDR, split_list
from packet import Packet

hashes = []
publishers = []
brokers = []


def select_other_broker(myself):
    if brokers == [myself]:
        return myself

    brk = list(brokers)
    brk.remove(myself)
    return random.choice(brk)


class Broker(DatagramProtocol):
    def __init__(self, name, receiver=False):
        super().__init__()
        self._send_loop = LoopingCall(self._load)
        self.name = name
        self.receiver = receiver

    def _load(self):
        _, pub_to_move = split_list(publishers)
        for pub in pub_to_move:
            other_home_broker = select_other_broker(self.name)
            print("Load! Telling {} to change home broker to {}.".format(pub, other_home_broker))
            p = Packet(self.name, '', pub, 'HomeBrokerChange', other_home_broker)
            self.transport.write(p.pack(), MCAST_ADDR)

    def startProtocol(self):
        self.transport.setTTL(5)
        self.transport.joinGroup(MCAST_IP)

        if not self.receiver:
            self._send_loop.start(interval=30, now=False)

    def datagramReceived(self, datagram, address):
        sender, broker, receiver, typ, data = Packet.unpack(datagram)

        if self.receiver and sender != self.name:
            h = hash(str([sender, broker, receiver, typ, data]))

            if typ == 'Message' and h not in hashes and broker == '':
                p = Packet(sender, self.name, '', 'Message', data)
                self.transport.write(p.pack(), MCAST_ADDR)
                hashes.append(h)
                if sender not in publishers:
                    publishers.append(sender)

            if typ == 'Message' and h not in hashes and broker != '':
                p = Packet(sender, self.name, '', 'Message', data)
                self.transport.write(p.pack(), MCAST_ADDR)
                hashes.append(h)
                if broker not in brokers:
                    brokers.append(broker)
                print("Brokers:")
                print(brokers)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Broker')
    parser.add_argument('name')
    args = parser.parse_args()

    reactor.listenMulticast(MCAST_PORT, Broker(args.name, receiver=True), listenMultiple=True)
    reactor.listenMulticast(MCAST_PORT, Broker(args.name), listenMultiple=True)
    reactor.run()
