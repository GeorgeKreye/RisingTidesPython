"""
Incomplete flood-fill module for the project. Should be replaced with RisingTidesComplete if the objective of an
assignment variant is not to complete this module.
"""

# import(s) go here
from typedefs import GridLocation


def flooded_regions_in(terrain: list[list[float]], sources: list[GridLocation], water_height: float):
    """
    Given a matrix of terrain heights, a list of water source tiles, and a water height, finds which
    terrain tiles should be considered flooded.
    :param terrain: A matrix of float values representing the elevations of each terrain tile
    :param sources: A list of grid locations representing to locations of water source tiles
    :param water_height: The water level at which tiles at or below this elevation should be considered
     to be flooded
    :return: A matrix of boolean values representing whether a terrain tile is flooded; an entry
     with a value of ``true`` means that tile is flooded
    """
    # create output grid of flooded tiles
    # each flooded tile is represented by a boolean, with a value of true
    flooded = [([False for j in terrain[0]]) for i in terrain]

    # TODO: Using breadth-first search, write an algorithm that finds all tiles that are at or below the
    #  water height and floods them. Depth-first search is also usable, but not as realistic.

    # return output grid
    return flooded
