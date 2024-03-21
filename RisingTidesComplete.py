"""
Completed version of the flood-fill module of the project. Should not be present if student assignment is to complete
RisingTides.py.
"""

# imports
from typedefs import GridLocation
from typing import TypeVar, Generic

# type var declaration
T = TypeVar('T')


class SearchQueue(Generic[T]):
    """
    A basic queue constructed using a list containing elements of type T. Used by this solution to
    handle search queueing; however, the builtin queue should work as well.
    """

    def __init__(self, starting_queue: list[T] = None):
        """
        Creates a search queue. Defaults to being empty
        (i.e. ``if starting_queue is None: starting_queue = []``).
        """
        if starting_queue is None:
            starting_queue = []
        self.queue: list[T] = starting_queue

    def enqueue(self, item: T):
        """
        Enqueues an item onto the search queue.
        :param item: The item to enqueue
        :return:
        """
        self.queue.append(item)

    def dequeue(self):
        """
        Dequeues the first item on the search queue.
        :return: The value of the removed item
        """
        # get value of item to be removed
        value = self.queue[0]

        # remove first item by shifting all items to the left one
        new_queue = []
        for i in range(1, len(self.queue)):
            new_queue.append(self.queue[i])
        self.queue = new_queue

        # return removed value
        return value

    def is_empty(self):
        """
        Checks whether this queue is currently empty.
        :return: ``true`` if the queue is empty (length 0)
        """
        return len(self.queue) == 0

    def size(self):
        """
        Gets the current size of the queue, determined by the number of elements within it.
        :return: An integer representing the current size of the queue
        """
        return len(self.queue)


def get_neighbors(center: GridLocation, terrain: list[list[float]]):
    """
    Helper function that given a grid location, finds its neighbors along the row and column it is in.
    :param center: The tile to find the neighbors of
    :param terrain: The full terrain array; size is used for neighbor validity bounds determination
    :return: A list of all valid neighboring grid locations
    """
    # get neighboring tiles
    left = GridLocation(center.row - 1, center.col)
    right = GridLocation(center.row + 1, center.col)
    down = GridLocation(center.row, center.col - 1)
    up = GridLocation(center.row, center.col + 1)

    # check if neighboring tiles are valid; if so, add to output
    out = []
    if left.in_bounds(len(terrain), len(terrain[0])):
        out.append(left)
    if right.in_bounds(len(terrain), len(terrain[0])):
        out.append(right)
    if down.in_bounds(len(terrain), len(terrain[0])):
        out.append(down)
    if up.in_bounds(len(terrain), len(terrain[0])):
        out.append(up)

    # return all valid tiles
    return out


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

    # create queue
    search_queue = SearchQueue[GridLocation]()

    # process water sources
    for source in sources:
        # make sure water source would actually create water
        if terrain[source.row][source.col] <= water_height:
            # set source tile as flooded and enqueue
            flooded[source.row][source.col] = True
            search_queue.enqueue(source)

    # process rest of tiles in main loop
    while not search_queue.is_empty():
        # dequeue first tile in queue
        current = search_queue.dequeue()

        # get neighboring tiles
        neighbors = get_neighbors(current, terrain)

        # process neighbor tiles
        for neighbor in neighbors:
            # check if neighbor tile should be flooded
            if terrain[neighbor.row][neighbor.col] <= water_height and not flooded[neighbor.row][neighbor.col]:

                # flood tile and add to queue
                flooded[neighbor.row][neighbor.col] = True
                search_queue.enqueue(neighbor)

    # return output grid of flooded tiles
    return flooded
