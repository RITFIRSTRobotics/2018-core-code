"""
Utility file for Networking

:author: Connor Henley @thatging3rkid
"""
import socket

# shamelessly stolen from https://stackoverflow.com/a/1267524
def get_ip():
    try:
        return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1][0]
    except:
        return "127.0.0.1"
