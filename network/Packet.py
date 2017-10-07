from enum import Enum

import sys


class Packet:
    """
    Contains data that is sent between the FMS and a robot
    """

    class StorageType(Enum):
        """
        Defines the type of data stored in a packet
        """

        COMMAND = 0
        STATUS = 1

        __slots__ = [COMMAND, STATUS]

    __type = None
    __data = None
    __slots__ = [__type, __data]

    def __init__(self, type):
        self.__type = type

    def get_data(self):
        """
        Return the data in the Packet

        :return: the data contained in the packet
        """
        return self.__data

    def __sizeof__(self):
        """
        Get the size of the Packet

        :return: the size of the object
        """
        return sys.getsizeof(self.__data) + sys.getsizeof(self.__type)
