from enum import Enum

class AllianceColor(Enum):

    NONE = 0
    RED = 1
    BLUE = 2

    @staticmethod
    def str_to_color(string):
        """
        Take a string and find the matching color

        :param string: a string containing a color (red or blue)
        :return: a Color based on the string
        """

        if string.lower().strip().startswith("r"):
            return AllianceColor.RED
        elif string.lower().strip().startswith("b"):
            return AllianceColor.BLUE
        else:
            return AllianceColor.NONE

    @staticmethod
    def color_to_string(color):
        """
        Take a color and find the matching string

        :param color: an AllianceColor
        :return: a string of the color
        """

        # Type check
        if type(color) is not AllianceColor:
            return None

        if color == AllianceColor.RED:
            return "r"
        elif color == AllianceColor.BLUE:
            return "b"
        else:
            return ""
