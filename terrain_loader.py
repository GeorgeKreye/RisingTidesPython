"""
Module which handles loading of terrain data from a .terrain file.
"""

# imports
from typedefs import *
import requests
import os
import hashlib
from pathlib import Path
from typing import TextIO
import traceback


def get_dimensions(file: TextIO):
    """
    Given a file input stream, reads in terrain dimension information.
    This will only work if used on an input stream belonging to a .terrain or .data file
    and if used in the proper order of reading lines from the file.
     :param file: The file input stream being read from
     :return: A list of integers containing the dimensional information
     """

    # get dimension information from file, convert information to integer format,
    # and place in output
    out = [-1, -1]  # -1 as placeholder
    for i in range(0, 2):
        out[i] = int(file.readline())

    if out[0] <= 0 and out[1] <= 0:
        raise BadValueError("Invalid dimension sizes " + str(out[0]) + " and " + str(out[1]))
    elif out[0] <= 0:
        raise BadValueError("Invalid dimension size " + str(out[0]))
    elif out[1] <= 0:
        raise BadValueError("Invalid dimension size " + str(out[1]))

    # return
    return out


def get_sources(file: TextIO, num_rows: int, num_columns: int):
    """
    Given a file input stream, reads in terrain water source(s) information.
    :param file: The file input stream being read from
    :param num_rows: The number of rows in the terrain dimensions; used for verifying
     that source coordinates are valid
    :param num_columns: The number of columns in the terrain dimensions; used for verifying
     that source coordinates are valid
    :return:
    """
    # get number of sources from file
    num_sources = int(file.readline())
    if num_sources <= 0:
        raise BadValueError("Invalid number of sources")

    # create sources list
    sources = []

    # fill sources list
    for i in range(0, num_sources):
        # get source row and column
        temp = file.readline().split()
        row = int(temp[0])
        if len(temp) == 1:
            col = int(file.readline())
        else:
            col = int(temp[1])

        # make sure row and column are within terrain dimensions
        if row < 0 or row >= num_rows:
            raise IndexError("Row {0} out of range [{1},{2})".format(row, 0, num_rows))
        if col < 0 or col >= num_columns:
            raise IndexError("Column {0} out of range [{1},{2})".format(col, 0, num_columns))

        # create GridLocation and add source to sources list
        sources.append(GridLocation(row, col))

    # return sources list when complete
    return sources


def read_heights(file: TextIO, num_rows: int, num_columns: int):
    # create empty heights matrix
    heights: list[list[float]] = []

    # read in height data
    data = []
    for line in file.readlines():
        s_line = line.split()
        for height in s_line:
            data.append(float(height))

    # sort height data into rows and columns within heights matrix
    for i in range(0, num_rows):
        row = []  # empty row in matrix to be filled
        for j in range(0, num_columns):
            row.append(data[j + (num_columns * i)])
        heights.append(row)  # add completed row to heights matrix

    # return sorted heights matrix
    return heights


def process_terrain_file(file: TextIO):
    """
    Processes data from a file stream into a Terrain object. The file stream should originate from a
    .data or .terrain file, otherwise unsupported behavior will occur.
    :param file: The file input stream being read from
    :return: A Terrain object
    """

    # check if file is remote
    source = file.readline().strip('\n')
    if source != "local":
        return load_web_terrain(source)

    # get terrain dimensions
    num_rows, num_columns = get_dimensions(file)

    # get source information
    sources = get_sources(file, num_rows, num_columns)

    # construct heights list
    heights = read_heights(file, num_rows, num_columns)

    # combine information into a terrain object
    terrain = Terrain(heights, sources)

    # return terrain
    return terrain


def is_key_for(key_file: Path, source: str):
    """
    Checks whether a given key file is the key for a given source URL, returning a
    boolean that reflects the result.

    The check is conducted by opening the key file from its path and checking if its
    first line matches the given source URL.

    If an OSError is raised due to the file being nonexistent or otherwise inaccessible,
    the method automatically returns ``false``.
    :param key_file: The path of the key file being checked
    :param source: The source URL
    :return: ``true`` if first line of key file matches source URL; ``false`` otherwise
    """
    try:
        # open key file
        stream = key_file.open()

        # determine if first line matches source URL
        output = stream.readline() == source

        # close key file and return
        stream.close()
        return output
    except OSError:
        # cannot access key file, so assume it is not the key file for the source URL
        return False


def load_web_terrain(source: str):
    """
    Given a source URL, attempts to retrieve a .data file stored in cache; if that fails,
    attempts to download the data into the cache by connecting to the source URL. If either succeeds,
    it will then pass the data file for processing
    :param source: The source URL
    :return: The Terrain object created by processing the data file
    """
    print("Attempting to load remote file " + source + " from cache")
    key_file = Path(os.path.join("DownloadCache", str(hashlib.sha1(source.encode()).hexdigest()) + ".key"))

    data_file = Path("DownloadCache/" + str(hashlib.sha1(source.encode()).hexdigest()) + ".data")

    # Check if download cache already contains the desired data from the URL
    if not key_file.is_file() or not data_file.is_file() or not is_key_for(key_file, source):
        print("Cache not found; attempting remote download from source")
        # attempt to download data from the URL
        with requests.get(source) as r:
            f = data_file.open("w")
            f.write(r.text)
            f.close()

        # if download is successful, make key file
        f = key_file.open("w")
        f.write(source)
        f.close()
        print("Download successful")
    else:
        print("File found in cache")

    # process from cache; can use same function as before as source is now local
    with data_file.open() as file:
        return process_terrain_file(file)


def get_available_terrain():
    """
    Gets a list of all terrain files that can be found in the 'terrains' directory.

    The function will automatically filter out files that are not .terrain files.
    :return: A list of strings representing the available terrain files
    """
    # get terrain directory contents
    files = os.listdir("terrains")

    # create output list
    out: list[str] = []

    # process contents
    for file in files:
        # split name and extension
        name, extension = file.split('.')

        # add file name to output list if it is a terrain file
        if extension == "terrain":
            out.append(name)

    # return completed list
    return out


def print_available_terrain():
    """
    Prints a list of available terrain files in 5-column rows.
    :return:
    """
    # get the terrain files that are found in the terrains directory
    files = get_available_terrain()

    # build output string to print
    out = ""
    col = 0  # counter used for determining when to add a newline
    for file in files:
        # add file name to output
        out += file
        # increment column or row
        if col == 4:  # increment row if col mod 5 is 4 (next col is part of a new row)
            out += "\n"
            col = 0
        else:
            out += " "
            col += 1

    # print output string
    print(out)


def load_terrain(filename: str):
    """
    Loads and processes the data of a .terrain file.

    The .terrain file must be located in the 'terrains' folder, otherwise loading the file
     will not succeed.
    :param filename: The name of the .terrain file, sans extension and path
    :return: None if an I/O error was raised, otherwise returns the processed data of the
     .terrain file as a Terrain object
    """

    # Get full path
    path = Path(os.path.join("terrains", filename + ".terrain"))

    # Attempt loading of file
    print("Loading file " + str(path))
    try:
        file = path.open("r")
        data = process_terrain_file(file)
        file.close()
        return data

    except OSError:
        # print error and return None
        print("Could not load " + str(path))
        traceback.print_exc()
        return None
