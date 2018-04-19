"""
Utility file for Networking

:author: Connor Henley @thatging3rkid
"""
import fcntl
import socket
import struct

# shamelessly stolen from https://stackoverflow.com/a/24196955
def get_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
