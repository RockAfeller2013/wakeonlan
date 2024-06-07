#!/usr/bin/env python3
# Usage: ./wakeonlan.py 74:56:3c:71:82:01
# Tested and working Wake on lan Magic Packet

import socket
import struct

def wake_on_lan(mac_address):
    # Check mac_address format and try to compensate.
    if len(mac_address) == 12:
        pass
    elif len(mac_address) == 12 + 5:
        sep = mac_address[2]
        mac_address = mac_address.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', mac_address * 20])
    send_data = b''

    # Split up the hex values into binary packets.
    for i in range(0, len(data), 2):
        send_data += struct.pack('B', int(data[i: i + 2], 16))

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('<broadcast>', 9))
    sock.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <MAC Address>")
        sys.exit(1)
    wake_on_lan(sys.argv[1])
