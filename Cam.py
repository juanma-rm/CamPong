# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

"""
Cam module

Takes charge of handling camera control, finding circles in frames,
determining which should correspond to each player and returning
the screen position where each player is pointing at
"""

# ------------------------------------------
# IMPORTS
# ------------------------------------------

try:
    import numpy as np
    import cv2
    from Constants import *
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame.time
except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# GLOBAL CONSTANTS
# ------------------------------------------

OFFSET_BOUND = 0.15

# Frame width
FRAME_X_POS = 1
FRAME_Y_POS = 0

# Circle params
CIRC_X = 0
CIRC_Y = 1
CIRC_RAD = 2

# ------------------------------------------
# GLOBAL VARIABLES
# ------------------------------------------

# ------------------------------------------
# FUNCTIONS DEFINITIONS
# ------------------------------------------

def cam_init():
    # Initialises the video flow
    vc = cv2.VideoCapture(0)
    return vc

def cam_process_circles(list_circles_candidates, frame_width, frame_height):

    # -----------------------
    # For bat, select bigger circle (in case several were found)
    # -----------------------

    max_circle_bat = None
    if ( len(list_circles_candidates) > 0):
        max_rad = 0
        for circle in list_circles_candidates:
            if (circle[CIRC_RAD] > max_rad):
                max_circle_bat = circle

    # -----------------------
    # Get positions projected on screen
    # -----------------------

    circle_screen_pos_x = None
    circle_screen_pos_y = None
    if (max_circle_bat is not None):
        # Convert circle coordinates from cam size (with offsets) to screen size
        # Axis X
        circle_cam_pos_x = max_circle_bat[CIRC_X]
        if (circle_cam_pos_x < OFFSET_BOUND*frame_width):
            circle_cam_pos_x = 0*frame_width
        elif (circle_cam_pos_x > (1-OFFSET_BOUND)*frame_width):
            circle_cam_pos_x = 1*frame_width
        else:
            circle_cam_pos_x = (1/(1*(1-2*OFFSET_BOUND)))*  \
                (circle_cam_pos_x-OFFSET_BOUND*frame_width) + 0
        circle_screen_pos_x = round(circle_cam_pos_x*SCREEN_W/frame_width)
        # Axis Y
        circle_cam_pos_y = max_circle_bat[CIRC_Y]
        if (circle_cam_pos_y < OFFSET_BOUND*frame_height):
            circle_cam_pos_y = 0*frame_height
        elif (circle_cam_pos_y > (1-OFFSET_BOUND)*frame_height):
            circle_cam_pos_y = 1*frame_height
        else:
            circle_cam_pos_y = (1/(1*(1-2*OFFSET_BOUND)))*  \
                (circle_cam_pos_y-OFFSET_BOUND*frame_height) + 0
        circle_screen_pos_y = round(circle_cam_pos_y*SCREEN_H/frame_height)

    return circle_screen_pos_x, circle_screen_pos_y

def cam_get_command(vc):
    # Analyses the current frame to determine the position of
    # each player within the camera frame size and converts those
    # positions to the screensize domain
    # Returns: (
    #   circle_1_screen_pos_x:Int, 
    #   circle_1_screen_pos_y:Int,
    #   circle_2_screen_pos_x:Int,
    #   circle_2_screen_pos_y:Int,
    #   state:Int
    # )

    # Ret variables
    state = CAM_STATE_UNKNOWN   # state by default
    circle_1_screen_pos_x = None
    circle_1_screen_pos_y = None
    circle_2_screen_pos_x = None
    circle_2_screen_pos_y = None

    # -----------------------
    # Get frame and find circles
    # -----------------------

    frame_is_ok, frame = vc.read()
    if (frame_is_ok == False):  # Frame not found
        state = CAM_STATE_NO_FRAME
    else: 
        frame_width = frame.shape[FRAME_X_POS]
        frame_height = frame.shape[FRAME_Y_POS]

        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred_frame = cv2.medianBlur(grey_frame, 25)
        # bilat_frame = cv2.bilateralFilter(grey_frame,10,50,50)

        # Method used: HoughCircles
        # Parameters:
        minDist = 30
        param1 = 150 # 500
        param2 = 50 # 200, smaller value, greater false circles
        minRadius = 10
        maxRadius = 100
        # circles = cv2.HoughCircles(grey_frame, cv2.HOUGH_GRADIENT, 1.2, 100)
        circles = cv2.HoughCircles(blurred_frame, cv2.HOUGH_GRADIENT, 1.2, minDist,   \
            param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

        if (circles is None):    # No circles found
            state = CAM_STATE_NO_CIRCLES
        else:

            # -----------------------
            # Filter the circles
            # -----------------------

            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # Cam image is mirrored in horizontal (X) axis
            circles_mirrored = []
            for circle in circles:  # circle = (x, y, r)
                circle_mirrored =   \
                    (frame_width - circle[CIRC_X], circle[CIRC_Y], circle[CIRC_RAD])
                circles_mirrored.append(circle_mirrored)

            # Circles in left for bat1 and circles in right for bat2
            list_circles_candidates_bat1 = []
            list_circles_candidates_bat2 = []
            for circle in circles_mirrored:  # circle = (x, y, r)
                if (circle[CIRC_X] < frame_width/2):
                    list_circles_candidates_bat1.append(circle)
                else:
                    list_circles_candidates_bat2.append(circle)
            
            circle_1_screen_pos_x, circle_1_screen_pos_y = \
                cam_process_circles(list_circles_candidates_bat1,frame_width, frame_height)
            circle_2_screen_pos_x, circle_2_screen_pos_y =  \
                cam_process_circles(list_circles_candidates_bat2,frame_width, frame_height)

    return (circle_1_screen_pos_x, circle_1_screen_pos_y,   \
        circle_2_screen_pos_x, circle_2_screen_pos_y, state)

# ------------------------------------------
# MAIN ALGORITHM
# ------------------------------------------

def cam_main(t0_exit, t1_queue):
    clock = pygame.time.Clock()
    prev_time_ms = 0
    vc = cam_init()
    if (vc is None or not vc.isOpened()):
        t0_exit.put((EXIT_ERR, "camera not working"))
    else:
        while(1):
            # Get new positions of players objects and send to GUI via queue
            circle_1_screen_pos_x, circle_1_screen_pos_y, circle_2_screen_pos_x,    \
                circle_2_screen_pos_y, state = cam_get_command(vc)
            t1_queue.put([circle_1_screen_pos_x, circle_1_screen_pos_y,     \
                circle_2_screen_pos_x, circle_2_screen_pos_y, state])
            # Timing 
            clock.tick(FPS)
            if (SHOW_REAL_FPS):
                real_fps = int(1000 / (pygame.time.get_ticks() - prev_time_ms))
                print("Cam fps: " + str(real_fps))
            prev_time_ms = pygame.time.get_ticks()