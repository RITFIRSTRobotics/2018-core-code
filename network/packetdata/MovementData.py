class MovementData:

    __lstick = 0
    __rstick = 0

    __slots__ = [__lstick, __rstick]

    def __init__(self, lstick, rstick):
        self.__lstick = lstick
        self.__rstick = rstick

    def get_fullmovement(self):
        return self.__lstick, self.__rstick

    def get_lstick(self):
        return self.__lstick

    def get_rstick(self):
        return self.__rstick
