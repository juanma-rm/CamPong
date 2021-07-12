# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

"""
CamPong main file

Instantiates and runs each task thread (GUI, camera, IA)
"""

# ------------------------------------------
# GLOBAL CONSTANTS
# ------------------------------------------

# Exceptions

# except SystemExit as err:
#     if (err.code != EMERGENCY):
#         raise  # normal exit, let unittest catch it
#     else:
#         os._exit(EMERGENCY)  # force stop



# ------------------------------------------
# IMPORTS
# ------------------------------------------

try:
    import sys
    import os
    import pygame
    import pygame.locals
    import math
    import random
    import getopt
    from socket import *
    from multiprocessing import Process, Queue
    import time as time
    import GUI
except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# CLASSES DEFINITIONS
# ------------------------------------------

def func1():
    print("Hello from GUI")

# ------------------------------------------
# GLOBAL DATA
# ------------------------------------------

# Task 0: main (this)

t0main_start = -1   # Queue?? --> to T1, T2, T3, T4

# Task 1: Img acquisition and processing (from T1)

# t1cam_process = Process(target=func1, args=(queue,))
t1cam_bat1_posx = -1    # --> to T3
t1cam_bat1_posy = -1    # --> to T3
t1cam_bat2_posx = -1    # --> to T3
t1cam_bat2_posy = -1    # --> to T3
t1cam_cam_working = False   # --> to ??

# Task 2: keyboard (from T2)        EMBEDDED IN TASK 3

# t2keyb_queue_evts_bat1 = Queue() # U, D, L, R --> to T3
# t2keyb_queue_evts_bat2 = Queue() # U, D, L, R --> to GUI
# t2keyb_process = Process(target=CamPong_Keyboard.keyboard, args=(t2keyb_queue_evts_bat1,t2keyb_queue_evts_bat2))

                        # ??? TO DEFINE
# Task 3: GUI

t3gui_process = Process(target=GUI.gui_pong)
t3gui_enable = False    # --> to T1
t3gui_nb_human_players = -1 # 0 (2 IAs), 1 (1 IA, 1 human), 2 (2 humans), -1 (not initialized)
                            # to T0, T1, T4
t3gui_control_type = -1 # --> to T1, T2
                        # ??? create constants to define two controls (cam and keyboard)
t3gui_new_game = None   # --> to T1, T2, T3
                        # ??? Queue?            
t3gui_ball_pos = None   # --> to T4
                        # ??? TO DEFINE
t3gui_ball_speed = None # --> to T4
                        # ??? TO DEFINE

# Task 4: IA

# t4ia_process = Process(target=func1, args=(queue,))
t4ia_bat1_pos = None    # --> to T3
t4ia_bat1_speed = None  # --> to T3
t4ia_bat2_pos = None    # --> to T3
t4ia_bat2_speed = None  # --> to T3
                        # ??? TO DEFINE ALL BAT POS/SPEED. Should IA control the pos? Or just the speed?




# ------------------------------------------
# FUNCTIONS DEFINITIONS
# ------------------------------------------

def main():
    # Create threads / queues / etc (in data section the better)

    # Run GUI
    t3gui_process.start()


    # tests


    while(1):
        
        # tests
        pass

            

        # Wait for new_game event
        # If new_game event arrives:
        #   Delete current threads for task1/2/4
        #   Run thread for task1 / task2 / task4 (according to game parameters)
        #   Take new events from tasks1/2/4 forward to task3. (This should be automatic; events from tasks 1/2/4 should go directly to task3)
        #   Start new game according to parameters (notify task3)
        # If exit_game event arrives:
        #   Kill current threads for task1/2/3/4 and main

# ------------------------------------------
# MAIN FLOW
# ------------------------------------------

if __name__ == '__main__':
    main()
