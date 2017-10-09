class MovementData:

    __slots__ = ["lstick", "rstick"]

    def __init__(self, lstick, rstick):
        self.lstick = lstick
        self.rstick = rstick

    def get_fullmovement(self):
        return self.lstick, self.rstick
