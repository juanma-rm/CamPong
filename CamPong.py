# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

"""
CamPong main file

Instantiates and runs each task thread (GUI, camera), after
having decoded input args (nb of players and control type)
"""

# ------------------------------------------
# IMPORTS
# ------------------------------------------

from Constants import *

try:
    import sys
    from multiprocessing import Process, Queue
    import argparse
    import Constants
    import GUI
    import Cam
except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# FUNCTIONS DEFINITIONS
# ------------------------------------------

def main(nb_players, player_control):
    
    # Task 0: main (this)
    t0_exit = Queue()

    # Task 1: Img acquisition and processing (from T1)
    t1_queue = Queue()
    t1cam_process = Process(target=Cam.cam_main, args=(t0_exit,t1_queue))  # --> to T3

    # Task 2: keyboard
    # Embedded in task 3

    # Task 3: GUI
    t3gui_process = Process(target=GUI.gui_pong,    \
        args=(t0_exit, t1_queue, nb_players, player_control))

    # Task 4: IA
    # Embedded in task 3

    # Run GUI
    if (player_control == CONTROLLER_CAM):
        t1cam_process.start()
    t3gui_process.start()

    while(1):
        # If exit, display exit message, close process and close whole app
        if (not t0_exit.empty()):
            exit_tuple = t0_exit.get()
            if (exit_tuple[0] == EXIT_SUC):
                print("\nExiting by user request...")
            elif (exit_tuple[0] == EXIT_ERR):
                print("\nerror: " + exit_tuple[1] + ". Exiting...")
            if (player_control == CONTROLLER_CAM):
                t1cam_process.kill()
            t3gui_process.kill()
            sys.exit(exit_tuple[0])

# ------------------------------------------
# ENTRY POINT
# ------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run CamPong.py')
    parser.add_argument("nb_players", type=int, default=1,
        help="Number of human players (0, 1 or 2); \
        the other(s) player(s) will be IA(s)")
    parser.add_argument("player_control", type=int, default=CONTROLLER_KEYB,
        help="Type of control: " + str(CONTROLLER_KEYB) + \
            " keyboard, " + str(CONTROLLER_CAM) + " camera")
    args = parser.parse_args()
    if (args.nb_players >=0 and args.nb_players <= 2):
        nb_players = args.nb_players
    else:
        nb_players = NB_PLAYERS_DEF
    if (args.player_control == CONTROLLER_KEYB or args.player_control==CONTROLLER_CAM):
        player_control = args.player_control
    else:
        player_control = CONTROLLER_DEF
    main(nb_players, player_control)