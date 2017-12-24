from enum import Enum


class StorageType(Enum):
    """
    Defines the type of data stored in a packet
    """

    REQUEST = 0, 'request'
    RESPONSE = 1, 'response'
    STATUS = 2, 'status'

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
