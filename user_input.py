"""
Module which handles user input that is not received from the console.
"""

# import
from dudraw import *

STEP_SIZE_INCREMENT = 0.1  # the increment with which to increase or decrease step size


def tick(water_height: float, step_size: float):
    """
    Checks for any user input that has occurred since the last time this function was called
    (or the start of execution).
    :param water_height: The current water level
    :param step_size: The current step size for changing the water level
    :return: A list representing whether to stop the program (escape was pressed), the water level after any
    input-caused changes were processed, and any changes to the step size
    """

    # create output list
    output = [False, water_height, step_size]

    # get all key events that have been received
    key_events = keys_typed()

    # process key events in order
    for key_event in key_events:
        if key_event == "":  # stop running program
            output[0] = True
            break  # no need to process additional key events if stopping execution
        elif key_event == '=' or key_event == '+':  # add to water level
            print("Increasing water level")
            output[1] = output[1] + output[2]
        elif key_event == '-' or key_event == '_':  # subtract from water level
            print("Decreasing water level")
            output[1] = output[1] - output[2]
        elif key_event == ']' or key_event == '}':  # add to step size
            print("Increasing step size")
            output[2] = output[2] + STEP_SIZE_INCREMENT
        elif key_event == '[' or key_event == '{':  # subtract from step size
            print("Decreasing step size")
            output[2] = output[2] - STEP_SIZE_INCREMENT

    # return
    return output
