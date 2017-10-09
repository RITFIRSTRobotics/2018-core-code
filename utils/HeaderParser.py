from enum import Enum

import sys


class HeaderParser:
    """
    Parses .h and .hpp files for #defines and makes a dict of the contents
    """

    contents = None

    def __init__(self, path):
        # Make sure path is a string
        if type(path) is not str:
            raise TypeError("HeaderParser: not given a string")

        if path.find(".h") is -1:
            print("HeaderParser: not a header file", file=sys.stderr)

        self.contents = dict()

        # Open the file
        file = open(path, 'r')
        self.__parse(file)

    def __parse(self, file):
        """
        Parses the file to make a dict
        """

        contents = file.read().strip()  # Read the header into memory
        file.close()  # Don't need the file anymore

        # Parse the file the right way (using a state machine)
        # First, we need to make a bunch of states
        class State(Enum):
            FS_DETECTED = 0  # Forward-slash detected
            INBL_COMMENT = 1  # In a block comment
            INLN_COMMENT = 2  # In a line comment
            PP_COMMAND = 3  # Preprocessor command detected
            IN_CODE = 4  # In code, nothing needs to be done
            BL_AST_DETECTED = 5  # In a block comment and an asterisk was detected
            PP_DEFINE = 6 # A #define command has been found
            PP_DEFINE_VALUE = 7 # Getting the value from a #define command

            pass

        # Next, instantiate some variables
        cstate = State.IN_CODE
        name = ""
        value = ""

        # Now, time to get processing
        for char in contents:

            ### States for detecting the start of a comment

            if char == '/' and cstate != State.FS_DETECTED:  # State for when a comment might have been detected
                cstate = State.FS_DETECTED
                continue

            if cstate == State.FS_DETECTED and char == '*':  # State for detecting block comments
                cstate = State.INBL_COMMENT
                continue

            if cstate == State.FS_DETECTED and char == '/':  # State for detecting line comments
                cstate = State.INLN_COMMENT
                continue

            if cstate == State.FS_DETECTED:  # Revert the state if a comment was not detected
                cstate = State.IN_CODE
                continue

            ### States for detecting the end of a comment

            if cstate == State.INBL_COMMENT and char == '*':  # State for escaping block comments
                cstate = State.BL_AST_DETECTED
                continue

            if cstate == State.BL_AST_DETECTED and char == '/':  # State for escaping block comments
                cstate = State.IN_CODE
                continue

            if cstate == State.BL_AST_DETECTED:  # State for when a block comment was not completed
                cstate = State.INBL_COMMENT
                continue

            if cstate == State.INLN_COMMENT and char == '\n':  # State for escaping line comments
                cstate = State.BL_AST_DETECTED
                continue

            ### States for detecing preprocessor commands

            if cstate == State.IN_CODE and char == '#': # State for detecting the beginning of a preprocessor command
                cstate = State.PP_COMMAND
                continue

            if cstate == State.PP_COMMAND and char != ' ': # State for figuring out the name of the command
                name += char
                continue

            if cstate == State.PP_COMMAND and char == ' ': # State for figuring out the name of the command
                if name.strip() == "define":
                    cstate = State.PP_DEFINE
                else:
                    cstate = State.IN_CODE
                name = ""
                continue

            ### States for the #define command

            if cstate == State.PP_DEFINE and char != ' ': # State for getting the name of the #define
                name += char
                continue

            if cstate == State.PP_DEFINE and char == ' ': # State for getting the value of the #define
                cstate = State.PP_DEFINE_VALUE
                continue

            if cstate == State.PP_DEFINE_VALUE and (char != ' ' and char != '\n'): # State for getting the value of the #define
                value += char
                continue

            if cstate == State.PP_DEFINE_VALUE and (char == ' ' or char == '\n'): # State for processing the value of the #define
                cstate = State.IN_CODE

                if value.startswith("\"") and value.endswith("\""):
                    # value is a string
                    self.contents[name] = str(value[1:-1])
                elif value.replace("-", "").strip().isdigit():
                    # value is an int
                    self.contents[name] = int(value)
                elif value.replace("-", "").strip().isdecimal():
                    # value is a floating point
                    self.contents[name] = float(value)
                elif value.strip() is "true" or value.strip() is "false":
                    # value is a boolean
                    self.contents[name] = bool(value.strip().capitalize())
                elif value.startswith("\'") and value.endswith("\'"):
                    # value is a character
                    self.contents[name] = str(value[1:-1])
                else:
                    raise SyntaxWarning("HeaderParser: can not detect type of \'" + value + "\'")

                name = ""
                value = ""

        pass
