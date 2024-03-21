"""
Main project module which is used to handle execution of the entire program.
"""

# imports
import time
from display import Display, display_closed
import user_input
import terrain_loader

# constants
DEFAULT_WATER_HEIGHT = 0.0  # default water level
DEFAULT_STEP_SIZE = 1.0  # default step size for changing water level
FRAME_LENGTH = 1000 / 60  # length of draw frame


def main():
    """
    Main function; initializes the display and loads the initial terrain before entering
    the main loop
    :return:
    """

    # set initial water level
    current_water_height = DEFAULT_WATER_HEIGHT

    # set initial step size
    current_step_size = DEFAULT_STEP_SIZE

    # Ask user for terrain file to load
    print("Available terrain files:")
    terrain_loader.print_available_terrain()
    valid_terrain = False
    terrain = ""
    while not valid_terrain:  # loop until a valid terrain file is selected
        terrain = input("Enter name of the terrain file you wish to load (no file extension): ")
        if terrain in terrain_loader.get_available_terrain():  # make sure terrain file exists in directory
            valid_terrain = True
        else:
            print("Terrain file \"{0}.terrain\" could not be found. Make sure no spelling mistakes are present and "
                  "the file exists in the terrains directory, then try again.".format(terrain))

    # load terrain
    current_terrain = terrain_loader.load_terrain(terrain)

    # create window
    print("Creating display")
    try:
        display_window = Display(current_terrain, current_water_height, current_step_size)
    except RuntimeError as E:
        raise RuntimeError("Could not create display") from E

    # main loop
    while True:
        #  check for input (change of water height or water height change step size)
        old_water_height = current_water_height
        old_step_size = current_step_size
        stop, current_water_height, current_step_size = user_input.tick(current_water_height, current_step_size)
        if stop:
            break
        if old_water_height != current_water_height:
            display_window.change_water_height(current_water_height)
        if old_step_size != current_step_size:
            display_window.change_step_size(current_step_size)

        # render frame
        display_window.render(FRAME_LENGTH)
        time.sleep(FRAME_LENGTH / 1000)  # frame delay

    print("Stopping!")
    del display_window
    display_closed()


# call main function on run
if __name__ == '__main__':
    main()
