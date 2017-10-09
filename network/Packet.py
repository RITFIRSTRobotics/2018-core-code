from enum import Enum

import sys


class Packet(object):
    """
    Contains data that is sent between the FMS and a robot
    """

    class StorageType(Enum):
        """
        Defines the type of data stored in a packet
        """

        REQUEST = 0
        RESPONSE = 1
        STATUS = 2


        __slots__ = [REQUEST, RESPONSE, STATUS]

    __slots__ = ["type", "data"]

    def __init__(self, type, data):
        self.type = type
        self.data = data
