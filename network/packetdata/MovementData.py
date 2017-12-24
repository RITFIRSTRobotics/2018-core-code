"""
Movement data sent from the FMS to the robot

:author: Connor Henley, @thatging3rkid
"""
from core.network.constants import CONTROLLER_DEADZONE
from core.network.packetdata.PacketData import PacketData


class MovementData(PacketData):

    __slots__ = ["stick_x", "stick_y", "scaled"]

    def __init__(self, stickx, sticky):
        PacketData.__init__(self)
        self.stick_x = stickx
        self.stick_y = sticky
        self.scaled = False

    def scale(self):
        if not self.scaled:
            self.stick_x -= 128  # bring the number into the signed realm
            self.stick_y -= 128  # bring the number into the signed realm
            self.scaled = True
