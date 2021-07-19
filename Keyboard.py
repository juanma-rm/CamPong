# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

"""
Keyboard module

Get events from keyboard
"""

# ------------------------------------------
# IMPORTS
# ------------------------------------------

try:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"    
    import pygame
    from Constants import *
except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# FUNCTIONS DEFINITIONS
# ------------------------------------------

def get_key_events():
    # Get events from keyboard and returns events for bats
    # Returns key_events:[Int,Int] = [bat1_ev, bat2_ev]

    key_events = [0,0]  # (bat1_move_dir, bat2_move_dir)
    keys=pygame.key.get_pressed()
    if keys[KEY_BAT1_UP]:
        key_events[0] = BAT_GO_UP_ID
    elif keys[KEY_BAT1_DOWN]:
        key_events[0] = BAT_GO_DOWN_ID
    if keys[KEY_BAT2_UP]:
        key_events[1] = BAT_GO_UP_ID
    elif keys[KEY_BAT2_DOWN]:
        key_events[1] = BAT_GO_DOWN_ID

    return key_events