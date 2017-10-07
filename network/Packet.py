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

        REQUEST = 0
        RESPONSE = 1
        STATUS = 2


        __slots__ = [REQUEST, RESPONSE, STATUS]

    __type = None
    __data = None
    __slots__ = [__type, __data]

    def __init__(self, type, data):
        self.__type = type
        self.__data = data

    def get_data(self):
        """
        Return the data in the Packet

        :return: the data contained in the packet
        """
        return self.__data

    def get_type(self):
        return self.__type

    def __sizeof__(self):
        """
        Get the size of the Packet

        :return: the size of the object
        """
        return sys.getsizeof(self.__data) + sys.getsizeof(self.__type)
