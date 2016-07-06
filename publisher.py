#!/usr/bin/env python3
import socket
import sys

import struct

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} (<broker_host>:<broker_port>) [(<broker_host>:<broker_port>) ...] '.format(
            __file__), file=sys.stderr)
        sys.exit(3)

    broker_host, broker_port = sys.argv[1].split(':')
    broker_port = int(broker_port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((broker_host, broker_port))
        except ConnectionRefusedError as e:
            print('Could not establish connection to broker. Exiting...', file=sys.stderr)
            sys.exit(4)

        while True:
            line = sys.stdin.readline().rstrip('\n')
            if line in [':exit', ':q', ':quit']:
                break

            data = line.encode('utf-8')
            data_length = len(data)

            msg = struct.pack('>I', data_length) + data
            sock.sendall(msg)
