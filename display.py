"""
Project module that handles graphical display as well as flooding updates due to being convenient to run in this module.
"""
# imports
from dudraw import Color
import dudraw
from typedefs import *
from RisingTidesComplete import flooded_regions_in
import math

# constants
WATER_COLOR = Color(0, 49, 83)  # water is colored prussian blue
BASE_WINDOW_SIZE = (1000, 800)  # window size before aspect ratio tweaking
INFOBOX_SPACE = 100  # y-area of window reserved for listing controls; also applied to x to maintain aspect ratio


class RGBPoint:
    """
    Class used to store an RGB color value alongside an associated threshold.
    """

    def __init__(self, r: int = 255, g: int = 255, b: int = 255, t: float = 0):
        """
        Creates a new RGBPoint object with the given RGB value and threshold.
        :param r: The red value of the color
        :param g: The green value of the color
        :param b: The blue value of the color
        :param t: The threshold associated with the given color
        :raises ValueError: If the given R, G, and/or B value is not in the range [0,256)
        """
        # ensure RGB values passed in are usable
        if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
            raise ValueError("RGB values can only be between 0 and 255")

        # create color object and assign values
        self.value = Color(r, g, b)
        self.threshold = t

    def __repr__(self):
        return "<RGBPoint value:{0} threshold:{1}>".format(self.value, self.threshold)

    def __str__(self):
        """
        When called using ``str(obj)``, returns the RGB value of the object as well as the threshold associated with it.
        :return: A string representing the RGB color of the RGBPoint as well as its threshold
        """
        return str(self.value) + " w/ threshold " + str(self.threshold)


class ThresholdGradient:
    """
    A gradient represented by a list of ``RGBPoint`` objects sorted in ascending order,
    with functions that allow for adding additional objects or interpolating between existing objects given a threshold.
    """

    def __init__(self, initial_colors: list[RGBPoint] = None):
        """
        Constructs a new threshold gradient object. Defaults to creating an empty gradient, but can be provided a list
        of ``RGBPoint`` objects to create a filled one.

        Warnings
        --------
        If provided an initial list of colors with thresholds to use in the new gradient, this function
        does NOT automatically sort them by ascending threshold, instead assuming they are already sorted that way.
        Using an unsorted list of ``RGBPoint`` objects to construct a threshold gradient object is unsupported behavior
        and may lead to unintended results.

        Parameters
        ----------
        initial_colors : list[RGBPoint] | None
            Optional; a sorted list of RGBPoint objects to use when constructing a new threshold gradient. Defaults to
             None, which creates an empty gradient.
        """
        # if no initial colors are passed in, create an empty gradient
        if initial_colors is None:
            initial_colors = []
        self.colors: list[RGBPoint] = initial_colors  # create gradient

    def __repr__(self):
        return "<ThresholdGradient colors:{0}>".format(self.colors)

    def __str__(self):
        """
        When called using ``str(obj)``, returns the list of RGBPoint objects stored in this ThresholdGradient object.
        :return: A string representing the list of RGBPoint colors in the gradient
        """
        return str(self.colors)

    def add_color(self, r: int = 255, g: int = 255, b: int = 255, t: float = 0):
        """
        Adds a color into the gradient with the given RGB value and threshold.
        :param r: The R value of the color
        :param g: The G value of the color
        :param b: The B value of the color
        :param t: The threshold where the new color should be located
        :return:
        :raises ValueError: if any of the RGB values are not in the range [0, 256) or if the threshold value ``t``
         is already used within the gradient
        """
        # ensure RGB values passed in are usable and that the passed in threshold
        # is not already occupied by another color
        if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
            raise ValueError("RGB values can only be between 0 and 255")
        for color in self.colors:
            if color.threshold == t:
                raise ValueError("Threshold value " + str(t) + " is already being used")

        # add color to gradient in the proper position
        added_early = False  # used to determine whether to append
        for i in range(0, len(self.colors)):
            if t < self.colors[i].threshold:
                added_early = True  # don't append, adding new value in the middle of the list

                # construct new gradient using colors from old gradient and the new value
                new_gradient = [self.colors[c] for c in range(0, i + 1)]  # list of colors before i initially
                temp = [self.colors[c] for c in range(i + 1, len(self.colors))]  # list of colors after i for extension
                new_gradient.append(RGBPoint(r, g, b, t))  # add new color to new gradient
                new_gradient.extend(temp)  # recombine temp list of colors after i with new gradient

                # overwrite gradient with new list and break loop
                self.colors = new_gradient
                break
        if not added_early:  # value was not added in the middle of the gradient list
            # new highest threshold, so append to end of gradient
            self.colors.append(RGBPoint(r, g, b, t))

    def get_color_by_threshold(self, t: float):
        """
        Given a threshold, retrieves the RGB color on the gradient associated with that threshold.

        If the given threshold does not have an exact match, the function will interpolate one from the colors the
        threshold sits between.
        :param t: The threshold at which to get the color on the gradient of
        :return: A ``Color`` object representing the RGB value at the given threshold
        :raises ValueError: if ``t`` is not within the bounds of the gradient
        """
        if t < self.colors[0].threshold or t > self.colors[len(self.colors) - 1].threshold:
            raise ValueError("given threshold is beyond the scope of the gradient")

        color = None
        for i in range(0, len(self.colors)):
            # check if current color has an equal or greater threshold compared to t
            if t <= self.colors[i].threshold:
                # determine where between the current color and the previous this threshold lies
                # 0.0 is if it matches the threshold of the previous color, 1.0 if it matches the threshold of the
                # current color
                progress = ((t - self.colors[i - 1].threshold) /
                            (self.colors[i].threshold - self.colors[i - 1].threshold))

                # determine tile color RGB values via interpolation
                r = int(_interpolate(
                    progress, 0, 1, self.colors[i - 1].value.get_red(), self.colors[i].value.get_red()))
                g = int(_interpolate(
                    progress, 0, 1, self.colors[i - 1].value.get_green(), self.colors[i].value.get_green()))
                b = int(_interpolate(
                    progress, 0, 1, self.colors[i - 1].value.get_blue(), self.colors[i].value.get_blue()))

                # set tile color
                color = Color(r, g, b)

                # break loop
                break
        if color is None:
            # must have hit upper end of loop, which should be impossible under normal behavior
            raise ValueError("given threshold is beyond the scope of gradient; not caught on initial check")

        # return color RGB value
        return color


class Tile:
    """
    A graphical tile used for displaying terrain information visually.
    """

    def __init__(self, x: int = 0, y: int = 0, w: float = 1, h: float = 1, color: Color = dudraw.WHITE):
        """
        Creates a new graphical tile object with the given data.
        :param x: The x location of the tile on the display coordinate plane; defaults to 0
        :param y: The y location of the tile on the display coordinate plane; defaults to 0
        :param w: The width of the tile; defaults to 1 unit on the display
        :param h: The height of the tile; defaults to 1 unit on the display
        :param color: The color the tile takes when drawn; defaults to ``dudraw.WHITE``
        """
        self.x = x  # x coordinate of tile
        self.y = y  # y coordinate of tile
        self.w = w  # width of tile
        self.h = h  # height of tile
        self.color = color  # color of tile

    def __repr__(self):
        return "<Tile x:{0} y:{1} w:{2} h:{3} color:{4}>".format(self.x, self.y, self.w, self.h, self.color)

    def __str__(self):
        """
        When called using ```str(obj)```, returns the coordinates, dimensions, and color of the tile in string form.
        :return: A string containing the x and y coordinates, width, height, and color of the tile
        """
        return "Tile: ({0}, {1}) with dimensions {2}x{3} and color {4}".format(self.x, self.y, self.w, self.h,
                                                                               self.color)

    def change_tile_color(self, new_color: Color):
        """
        Changes the tile color to a new color value.
        :param new_color: A ``Color`` object representing the color to now be used by the tile
        :return:
        """
        self.color = new_color

    def draw(self):
        """
        Draws the tile onto the display to be rendered later.
        :return:
        """
        # set draw color to this tile's color
        # if flooded, will always be blue; otherwise, will be the color associated with their elevation
        dudraw.set_pen_color(self.color)

        # draw to display
        dudraw.rectangle(self.x, self.y, self.w / 2, self.h / 2)


class Display:
    """
    Class used for changing the dudraw display used by the project.
    """
    display_exists = False  # whether a display has already been created

    def __init__(self, initial_terrain: Terrain, initial_water_height: float, initial_step_size: float):
        """
        Creates a new display object and initializes the display.
        :param initial_terrain: The terrain object to use to create the display
        :param initial_water_height: The current water height
        :param initial_step_size: The step size currently being used to change the water level; used for display only
        :raises RuntimeError: If a display window already exists
        """
        # make sure there isn't already an active display
        if Display.display_exists:
            raise RuntimeError("Cannot create a new display instance while one is active")

        # create empty tiles matrix
        self.tiles: list[list[Tile]] | None = None

        # create constant elevation gradient
        self.GRADIENT = _elevation_gradient()

        # set initial terrain data and water height
        self.terrain = initial_terrain
        self.water_height = initial_water_height
        self.step_size = initial_step_size  # step size stored for display only

        # calculate width, height, and aspect ratio
        width = BASE_WINDOW_SIZE[0]
        height = BASE_WINDOW_SIZE[1]
        aspect_ratio = len(self.terrain.heights[0]) / len(self.terrain.heights)

        # adjust width and height based on aspect ratio
        if width / height > aspect_ratio:
            width = height * aspect_ratio
        else:
            height = width / aspect_ratio

        # create window
        dudraw.set_canvas_size(width, height)
        dudraw.set_x_scale(0 - INFOBOX_SPACE / 2, len(self.terrain.heights[0]) + INFOBOX_SPACE / 2)
        dudraw.set_y_scale(0 - INFOBOX_SPACE, len(self.terrain.heights))
        Display.display_exists = True

        # draw
        self.draw(True)

    def change_water_height(self, new_water_height: float):
        """
        Changes the water level used to determine what tiles are flooded.
        :param new_water_height: An integer representing the new water height to use
        :return:
        """
        self.water_height = new_water_height
        self.draw(True)

    def change_step_size(self, new_step: float):
        """
        Changes the step size to be displayed to reflect the current one.
        :param new_step: The new step size to be displayed
        :return:
        """
        self.step_size = new_step
        self.draw(False)

    def draw(self, recalculate_flood: bool):
        """
        Draws the display into dudraw, so it can be rendered later.
        :return:
        """
        # clear display
        dudraw.clear(Color(102, 2, 60))  # background color (Tyrian purple)


        if recalculate_flood:
            # create tile display matrix
            self.tiles = _construct_tile_matrix(self.terrain.heights, self.GRADIENT)

            # determine which tiles are flooded
            print("Running flooding code\n"
                  "(NOTE: Even if correct, this may take a while to execute depending on the terrain)")
            _flood_tiles(self.tiles, self.terrain, self.water_height)

        # since a transformation into DUDraw's coordinate space is required, do that before drawing
        dudraw_tiles = list(self.tiles)
        dudraw_tiles.reverse()
        dudraw_tiles = _transpose_tiles(dudraw_tiles)  # switch rows and columns

        # draw tiles
        for row in dudraw_tiles:
            for tile in row:
                tile.draw()

        # draw infobox
        dudraw.set_pen_color(dudraw.WHITE)  # infobox color
        dudraw.filled_rectangle((len(self.terrain.heights[0]) + INFOBOX_SPACE / 2) / 2, -INFOBOX_SPACE / 2,
                                (len(self.terrain.heights[0]) + INFOBOX_SPACE / 2 / 2), INFOBOX_SPACE / 2)

        # draw infobox text
        dudraw.set_pen_color(dudraw.BLACK)  # infobox text color
        dudraw.set_font_size(20)
        dudraw.text(len(self.terrain.heights[0]) / 6.3, -INFOBOX_SPACE / 4,
                    "Water level: {0} (change with +/-)".format(self.water_height))
        dudraw.text(len(self.terrain.heights[0]) / 5, -2.5 * INFOBOX_SPACE / 4,
                    "Level change step size: {0} (change with ]/[)".format(self.step_size))

    def render(self, frame_length):
        """
        If there is data drawn into the dudraw display, renders it for a certain amount of time.
        :param frame_length: The amount of time the frame should be rendered for;
         should sync with desired frames per second
        :return:
        """
        # make sure display isn't empty (tiles should be drawn) before rendering
        if self.tiles is not None:
            dudraw.show(frame_length)  # render display to window


def display_closed():
    """
    Called to tell the Display class that the current active display was closed.
    :return:
    """
    Display.display_exists = False


def _elevation_gradient():
    """
    Helper function that constructs a constant threshold gradient for elevation display.
    :return: The fully constructed list of elevation gradient colors and their thresholds
    """
    # create gradient colors with thresholds
    # colors in order are: pakistan green - 0.0, chartreuse - 0.1, maize - 0.25, metallic gold - 0.4, and sienna - 1.01
    elevation_colors = [RGBPoint(0, 102, 0, 0.0), RGBPoint(154, 205, 50, 0.1),
                        RGBPoint(251, 236, 93, 0.25), RGBPoint(212, 175, 55, 0.4),
                        RGBPoint(166, 60, 20, 1.01)]

    # create gradient object
    gradient = ThresholdGradient(elevation_colors)

    # return
    return gradient


def _construct_tile_matrix(terrain_heights: list[list[float]], elevation_gradient: ThresholdGradient):
    """
    Helper function that constructs a matrix of display tiles from a matrix of terrain heights and a gradient for
    mapping color to elevation.
    :param terrain_heights: The matrix containing the height data of the terrain
    :param elevation_gradient: The threshold gradient used to determine the color of a tile at a specific height
    :return: A matrix of display tiles reflecting the input data
    """
    # calculate terrain maximum and minimum heights
    min_h = math.inf
    max_h = -math.inf
    for row in terrain_heights:
        for col in row:
            # check if current height is larger than maximum or lower than minimum
            if col > max_h:
                max_h = col
            elif col < min_h:
                min_h = col

    # create tile matrix
    tiles: list[list[Tile]] = []

    # fill matrix with tile objects
    for row in range(0, len(terrain_heights)):
        tiles.append([])  # create empty row
        for col in range(0, len(terrain_heights[row])):
            # calculate tile threshold
            t = _interpolate(terrain_heights[row][col], min_h, max_h, 0.0, 1.0)

            # create tile
            tile = Tile(row, col, 1, 1,
                        elevation_gradient.get_color_by_threshold(t))

            # add tile to matrix
            tiles[row].append(tile)

    # return completed matrix
    return tiles


def _flood_tiles(tiles: list[list[Tile]], terrain: Terrain, water_height: float):
    """
    Determines what tiles on the matrix are flooded and if any are, recolors them to the water color.
    :param tiles: The inputted tile matrix
    :param terrain: The terrain data used for both terrain elevation and water sources
    :param water_height: The current water level being used to determine flooding
    :return:
    """
    # get flooded tiles
    flooded = flooded_regions_in(terrain.heights, terrain.sources, water_height)

    # color flooded tiles
    for row in range(0, len(flooded)):
        for col in range(0, len(flooded[row])):
            if flooded[row][col]:
                tiles[row][col].change_tile_color(WATER_COLOR)


def _interpolate(value: float, i_min: float, i_max: float, o_min: float, o_max: float):
    """
    Helper function that maps a float ``value`` to an output range, given an input range to map using.
    The function assumes both the input and output arrays to use for mapping are of the form [``i_min``, ``i_max``]
    and [``o_min``, ``o_max``), respectively, and requires that ``value`` lies in the former range.
    :param value: The input float value to be interpolated
    :param i_min: The minimum value of the input range
    :param i_max: The maximum value of the input range
    :param o_min: The minimum value of the output range
    :param o_max: The maximum value of the output range
    :return: The interpolated float value within the output range [``o_min``, ``o_max``)
    :raises ValueError: If ``value`` is not within the range [``i_min``, ``i_max``], and therefore is unmappable
     in that context
    """
    # make sure value to be interpolated falls between original minimum and maximum
    if value < i_min or value > i_max:
        raise ValueError(str(value) + " is not in range [" + str(i_min) + "," + str(i_max) + ")")

    # calculate interpolated value and return
    return (value - i_min) / (i_max - i_min + 0.000001) * (o_max - o_min) + o_min


def _transpose_tiles(matrix: list[list[Tile]]):
    """
    Helper function that transposes a tile matrix (that is, makes its rows its columns and vice versa). The input matrix
    is not directly altered as to prevent unintended mutation as well as to allow the assignment of the transposed array
    to a new variable.

    The function will only compute the transpose if the matrix is rectangular - that is, all rows are of equal length.
    :param matrix: The input matrix to be transposed
    :return: The transposed matrix
    :raises ValueError: If the input matrix has unequal row lengths
    """
    # make sure matrix is rectangular before proceeding
    for i in range(1, len(matrix)):
        if len(matrix[i]) != len(matrix[i - 1]):
            raise ValueError("input array is not rectangular (uneven row lengths)")

    new_matrix = []  # create empty matrix that will contain the transposed input

    # perform transpose
    for col in range(0, len(matrix[0])):
        t_row = []
        for row in range(0, len(matrix)):
            t_row.append(matrix[row][col])
        new_matrix.append(t_row)

    # change individual tiles' coordinates to reflect transpose
    for x in range(0, len(new_matrix)):
        for y in range(0, len(new_matrix[x])):
            new_matrix[x][y].x = x
            new_matrix[x][y].y = y

    # return the transposed matrix
    return new_matrix
