"""
Movement data sent from the FMS to the robot

:author: Connor Henley, @thatging3rkid
"""
from core.network.packetdata.PacketData import PacketData


class MovementData(PacketData):

    def __init__(self, _rd):
        PacketData.__init__(self)
        self.sticks = _rd.sticks
        self.buttons = _rd.buttons
        self.scaled = False

    def scale(self):
        if not self.scaled:
            for i in range(self.sticks):
                self.sticks[i] -= 128  # bring the number into the signed realm
            self.scaled = True

    def get_stick0(self):
        return self.sticks[0], self.sticks[1]

    def get_stick1(self):
        return self.sticks[2], self.sticks[3]
