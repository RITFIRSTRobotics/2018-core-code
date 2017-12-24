from enum import Enum


class PacketType(Enum):
    """
    Defines the type of data stored in a packet
    """

    REQUEST = 0, 'request'  # A request for data
    RESPONSE = 1, 'response'  # A response from the request
    STATUS = 2, 'status'  # Some sort of status sent from the FMS
    DATA = 3, 'data'  # Data is not requested from the FMS, it is just sent

    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        return member

    def __int__(self):
        return int(self.value)

class Packet(object):
    """
    Contains data that is sent between the FMS and a robot
    """

    __slots__ = ["type", "data"]

    def __init__(self, type, data):
        self.type = type
        self.data = data
