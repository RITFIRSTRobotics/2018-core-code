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

        # Strip away comments
        # Start with block comments
        while True:
            # First, see if a block comment is here
            start = contents.find("/*")

            # If not, skip to the next section
            if start == -1:
                break
            else:
                # If so, find the end
                end = contents.find("*/", start)
                if end == -1:
                    # If the end doesn't exist, raise an error
                    raise SyntaxError("HeaderParser: error parsing " + str(file.name) + ": hit EOF")

                # Patch a new string together
                temp_string = contents[:]
                contents = temp_string[0:start] if start != 0 else ""
                contents += temp_string[end + 2:] if (end + 2) < len(temp_string) else ""

        while True:
            # See if a line comment exists
            start = contents.find("//")

            # If not, go to the next section
            if start == -1:
                break
            else:
                # Find the end of the line (ie end of the comment)
                end = contents.find("\n", start)

                # Make a new string
                temp_string = contents[:]
                contents = temp_string[0:start] if start != 0 else ""
                contents += temp_string[end + 1:] if end != -1 else ""

        # todo make a dict of the string so line numbers can be referenced -Connor
        # todo find \ characters and remove them

        # Clean up the string a little
        contents = contents.lstrip()

        process_ln = []
        depth = -1
        # Parse each line
        for line in contents.split("\n"):


            # ifdef stuffs
            if line.lstrip().startswith("#endif"):
                process_ln.pop(depth)
                depth -= 1

            if line.lstrip().startswith("#else"):
                process_ln[depth] = not process_ln[depth]


            if depth != -1:
                if not (process_ln[depth] == None or process_ln[depth] == True):
                    continue

            # See if the line starts with #define
            if line.lstrip().startswith("#define"):
                # Break the line into parts
                parts = line.lstrip().split(" ")

                # Get rid of empty parts (ie more than one space between things)
                temp_parts = parts[:] # Copy the list
                parts = [] # Make the list empty
                for part in temp_parts: # Go through the list and add things that are valid
                    if part.strip() != "":
                        parts.append(part)

                # Make sure there is a valid number of parts
                if len(parts) < 3:
                    raise SyntaxError("HeaderParser: error parsing line `" + str(line) + "`")

                # Figure out the type of the data
                name = parts[1]
                value = parts[2]
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
                continue

            # See if the line starts with an #ifdef
            if line.lstrip().startswith("#ifdef"):

                parts = line.lstrip().split(" ")
                # Get rid of empty parts (ie more than one space between things)
                temp_parts = parts[:]  # Copy the list
                parts = []  # Make the list empty
                for part in temp_parts:  # Go through the list and add things that are valid
                    if part.strip() != "":
                        parts.append(part)

                if len(parts) != 2:
                    raise SyntaxError("HeaderParser: error parsing line `" + str(line) + "`")

                if str(parts[1]) in self.contents:
                    process_ln.append(True)
                else:
                    process_ln.append(False)
                continue


        if depth != -1:
            raise SyntaxError("HeaderParser: reached EOF and depth is non-zero")

        pass
