"""
Data about the state of a robot

:author: Connor Henley, #thatging3rkid
"""
from enum import Enum

from core.network.packetdata.PacketData import PacketData


class RobotStateData(PacketData, Enum):
    ENABLE = 0, 'enable'  # robot should be enabled
    DISABLE = 1, 'disable'  # robot should be disabled
    E_STOP = -1, 'emergency stop'  # robot should be stopped, all outputs disabled, and requires a hardware restart
