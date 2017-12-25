import os
import sys


class HeaderParser:
    """
    Parses .h and .hpp files for #defines and makes a dict of the contents

    :author: Connor Henley @thatging3rkid
    """

    __slots__ = ["contents"]  # save a little memory

    def __init__(self, path):
        # Make sure path is a string
        if type(path) is not str:
            raise TypeError("HeaderParser: not given a string")

        # Make sure this is a header file
        if path.find(".h") is -1:
            print("HeaderParser: not a header file", file=sys.stderr)

        # Initialize the contents dict
        self.contents = dict()
        self.contents["__py_parser"] = 0  # define __py_parser so that stuff can be #ifndef'd out

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

                # Patch a new string together (keeping the number of newlines)
                temp_string = contents[:] # make a copy to take from
                num_newlines = contents.count("\n", start, end) # count the number of newlines
                contents = temp_string[0:start] if start != 0 else "" # add the pre-comment
                contents += "\n" * num_newlines # add the number of newlines
                contents += temp_string[end + 2:] if (end + 2) < len(temp_string) else "" # add the post-comment

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
                temp_string = contents[:] # make a copy to take from
                contents = temp_string[0:start] if start != 0 else "" # add the pre-comment
                contents += temp_string[end:] if end != -1 else "" # add the post-comment (keep the newline)

        process_ln = [] # keep track if code should be executed
        depth = -1 # keep track of the depth of the if statement
        # Parse each line
        lines = contents.split("\n")
        for i in range(0, len(lines)):
            line = lines[i]

            # Check for an #endif
            if line.lstrip().startswith("#endif"):
                process_ln.pop(depth)
                depth -= 1
                continue

            # Check for an #else
            if line.lstrip().startswith("#else"):
                process_ln[depth] = not process_ln[depth]
                continue

            # Skip the line if it should not be processed (ie #ifdef is false)
            if depth != -1:
                if not process_ln[depth] is None or process_ln[depth] is True:
                    continue

            # See if the line starts with #define
            if line.lstrip().startswith("#define"):
                # Break the line into parts
                parts = line.lstrip().split(" ")

                # Get rid of empty parts (ie more than one space between things)
                temp_parts = parts[:]  # Copy the list
                parts = []  # Make the list empty
                for part in temp_parts:  # Go through the list and add things that are valid
                    if part.strip() != "":
                        parts.append(part)

                # Make sure there is a valid number of parts
                if len(parts) < 2:
                    raise SyntaxError("HeaderParser: " + os.path.basename(file.name) + ":" + str(i + 1)
                                      + " not enough arguments for #define")

                # Just a `#define name` line
                if len(parts) == 2:
                    self.contents[parts[1]] = None

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
                    print("HeaderParser: " + os.path.basename(file.name) + ":" + str(i + 1)
                          + " type detection failed (added as str)", file=sys.stderr)
                    self.contents[name] = str(value)
                continue

            # See if the line starts with an #ifdef
            if line.lstrip().startswith("#ifdef"):
                depth += 1

                parts = line.lstrip().split(" ")
                # Get rid of empty parts (ie more than one space between things)
                temp_parts = parts[:]  # Copy the list
                parts = []  # Make the list empty
                for part in temp_parts:  # Go through the list and add things that are valid
                    if part.strip() != "":
                        parts.append(part)

                if len(parts) != 2:
                    raise SyntaxError("HeaderParser: " + os.path.basename(file.name) + ":" + str(i + 1)
                                      + " not enough arguments for #ifdfe")

                # See if the name has been read in already
                if str(parts[1]) in self.contents:
                    process_ln.append(True)
                else:
                    process_ln.append(False)
                continue

            # See if the line starts with an #ifndef
            if line.lstrip().startswith("#ifndef"):
                depth += 1

                parts = line.lstrip().split(" ")
                # Get rid of empty parts (ie more than one space between things)
                temp_parts = parts[:]  # Copy the list
                parts = []  # Make the list empty
                for part in temp_parts:  # Go through the list and add things that are valid
                    if part.strip() != "":
                        parts.append(part)

                if len(parts) != 2:
                    raise SyntaxError("HeaderParser: " + os.path.basename(file.name) + ":" + str(i + 1)
                                      + " not enough arguments for #ifdef")

                # See if this name doesn't exist
                if str(parts[1]) not in self.contents:
                    process_ln.append(True)
                else:
                    process_ln.append(False)
                continue

        # Make sure the depth is right
        if depth != -1:
            raise SyntaxError("HeaderParser: " + os.path.basename(file.name) +
                              " reached end-of-file and depth is non-zero")
