#!/usr/bin/env python3

import struct


class Packet(object):
    def __init__(self, sender, broker, receiver, type, data):
        self.sender = sender
        self.broker = broker
        self.receiver = receiver
        self.type = type
        self.data = data

    def pack(self):
        sender_enc = self.sender.encode()
        broker_enc = self.broker.encode()
        receiver_enc = self.receiver.encode()
        type_enc = self.type.encode()
        data_enc = self.data.encode()
        return struct.pack(
            ">IIIII{}s{}s{}s{}s{}s".format(len(sender_enc), len(broker_enc), len(receiver_enc), len(type_enc),
                                           len(data_enc)),
            len(sender_enc),
            len(broker_enc),
            len(receiver_enc),
            len(type_enc),
            len(data_enc),
            sender_enc,
            broker_enc,
            receiver_enc,
            type_enc,
            data_enc,
        )

    @staticmethod
    def retrieve_packet(packet):
        return Packet(*Packet.unpack(packet))

    @staticmethod
    def unpack(packet):
        sender_len = struct.unpack(">I", packet[0:4])[0]
        broker_len = struct.unpack(">I", packet[4:8])[0]
        receiver_len = struct.unpack(">I", packet[8:12])[0]
        type_len = struct.unpack(">I", packet[12:16])[0]
        data_len = struct.unpack(">I", packet[16:20])[0]
        return [x for x in
                map(lambda x: x.decode(),
                    struct.unpack(">{}s{}s{}s{}s{}s".format(sender_len, broker_len, receiver_len, type_len, data_len),
                                  packet[20:]))
                ]

    def __repr__(self):
        return 'Packet(' + ', '.join([self.sender, self.broker, self.receiver, self.type, self.data]) + ')'

    def __eq__(self, other):
        try:
            return all(getattr(self, key) == getattr(other, key)
                       for key in self.__dict__ if not key.startswith('_'))
        except AttributeError:
            return False


if __name__ == '__main__':
    assert ["Alice", "Broker1", "Bob", "Message", "Hello World"] == Packet.unpack(
        Packet("Alice", "Broker1", "Bob", "Message", "Hello World").pack())
