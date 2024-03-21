"""
Contains various type definitions that are used in multiple modules of the project.
"""


class GridLocation:
    """
    Contains a single (x,y) coordinate with no attached data.
    """

    def __init__(self, row: int, col: int):
        """
        Creates a grid coordinate object given two dimensions.
        :param row: The row/x coordinate of the grid location
        :param col: The column/y coordinate of the grid location
        """
        self.row = row
        self.col = col

    def in_bounds(self, max_r: int, max_c: int, min_r: int = 0, min_c: int = 0):
        """
        Checks whether this coordinate falls within a given set of bounds where the bounds of a
        coordinate are of the format [min,max).
        :param min_r: The minimum bound on the row/x coordinate; defaults to 0
        :param min_c: The minimum bound on the column/y coordinate; defaults to 0
        :param max_r: The maximum bound on the row/x coordinate
        :param max_c: The maximum bound on the column/y coordinate
        :return: ``true`` if this grid location falls within the given bounds
        """
        return min_r <= self.row < max_r and min_c <= self.col < max_c

    def __repr__(self):
        return "<GridLocation row:{0} col:{1}>".format(self.row, self.col)

    def __str__(self):
        """
        When called via ``str(obj)``, returns a coordinate pair to be printed as representing a GridLocation object.
        :return: A string representing the GridLocation as a set of coordinates
        """
        return "({0}, {1})".format(self.row, self.col)

    def as_list(self):
        """
        Returns the GridLocation as a list containing two integers.
        :return: A list containing the row and column of the GridLocation
        """
        return [self.row, self.col]

    def as_tuple(self):
        """
        Returns the GridLocation as a tuple containing two integers.
        :return: A tuple containing the row and column of the GridLocation
        """
        return self.row, self.col


class Terrain:
    """
    Stores the processed data associated with a .terrain file.
    """

    def __init__(self, heights: list[list[float]], sources: list[GridLocation]):
        """
        Creates a new Terrain object with required information.
        :param heights: A matrix containing this terrain's height information.
        :param sources: A list containing this terrain's water sources.
        """
        self.heights = heights
        self.sources = sources

    def __repr__(self):
        return "<Terrain heights:{0} sources:{1}".format(self.heights, self.sources)

    def __str__(self):
        """
        When called via ``str(obj)``, returns a matrix of heights as well as a list of sources.
        :return: The output string representing the Terrain object
        """
        # create empty output string
        string = ""

        # add heights to string
        string += "Heights:\n"
        for row in range(0, len(self.heights)):
            # create empty string for row
            row_str = ""

            # go through height values in row
            for col in range(0, len(self.heights[row])):
                # add coordinates and height value to string for row
                row_str += "({0},{1}): {2}".format(row, col, self.heights[row][col])
                if col < len(self.heights[row]) - 1:
                    row_str += ", "

            # add string for row to output string
            string += row_str + "\n"

        # add water sources to string
        string += "Sources:\n"
        for i in range(0, len(self.sources)):
            # add coordinates of source to output string
            string += str(self.sources[i])
            if i < len(self.sources) - 1:
                string += ", "

        # return completed output string
        return string


class BadValueError(IOError):
    """
    An I/O exception meant to be raised when a value that cannot be handled by a portion of the program,
    such as a function it is intended for, is received from a file.
    """

    def __init__(self, reason: str = "received a bad value for a parameter from a file"):
        """
        An I/O exception meant to be raised when a value that cannot be handled by a portion of the
        program, such as a function it is intended for, is received from a file.
         This constructor should be called in a ``raise`` statement.
        :param reason: A custom message to display; should be used to provide a more specific
         reason that the exception occurred. Defaults to 'received a bad value for a parameter from a file'.
        """
        self.reason = reason
        super().__init__(self.reason)  # pass to parent constructor

    def __repr__(self):
        return "<BadValueError reason:{0}>".format(self.reason)

    def __str__(self):
        """
        When called using ``str(obj)``, returns a string containing the name of the error class as well as the error
        reason.
        :return: A string containing the name of this error as well as the reason it was called
        """
        return "BadValueError: " + self.reason
