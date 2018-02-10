"""
Data that the FMS (or robot) requests from the other

:author: Connor Henley, @thatging3rkid
"""
from enum import Enum

from core.network.packetdata.PacketData import PacketData

class RequestData(Enum):
    STATUS = 0, 'status'  # FMS can ask the robot for it's status (enabled, disabled, etc)
    # todo add more states
