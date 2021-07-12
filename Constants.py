# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

# CamPong constants


# ------------------------------------------
# IMPORTS
# ------------------------------------------

try:
    import pygame.locals
    import math

except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# GLOBAL CONSTANTS
# ------------------------------------------

# Misc
GAME_VERSION = 0.1
FPS = 50
PI = math.pi
EMERGENCY = -1  # For exceptions

# Sizes
SCREEN_H = 720
SCREEN_W = 1280

# Colours
COLOUR_WHITE = (250, 250, 250)
COLOUR_RED = (200, 50, 50)
COLOUR_GREEN = (0, 150, 0)
COLOUR_BLACK = (10,10,10)
BACKG_COL = COLOUR_BLACK

# Keyboards
KEY_BAT1_UP = pygame.locals.K_w
KEY_BAT1_DOWN = pygame.locals.K_s
KEY_BAT1_LEFT = pygame.locals.K_a
KEY_BAT1_RIGHT = pygame.locals.K_d
KEY_BAT2_UP = pygame.locals.K_UP
KEY_BAT2_DOWN = pygame.locals.K_DOWN
KEY_BAT2_LEFT = pygame.locals.K_LEFT
KEY_BAT2_RIGHT = pygame.locals.K_RIGHT

# Mobile objects
BALL_ID = 0
BAT1_ID = 1
BAT2_ID = 2
BALL_VERT_BOUNCE = 1
BALL_HOR_BOUNCE = 2
BAT_GO_UP_ID = 1
BAT_GO_DOWN_ID = 2

# Collisions labels
# Border collisions
COLLISION_BOUND_TOP_ID = -1
COLLISION_BOUND_BOT_ID = -2
COLLISION_BOUND_LEFT_ID = -3
COLLISION_BOUND_RIGHT_ID = -4
# Side collisions (which side of the current obj has collided)
COLLISION_TOP = -1
COLLISION_BOT = -2
COLLISION_LEFT = -3
COLLISION_RIGHT = -4
# Bat-ball collisions
COLLISION_BAT_1_5 = 1
COLLISION_BAT_2_5 = 2
COLLISION_BAT_3_5 = 3
COLLISION_BAT_4_5 = 4
COLLISION_BAT_5_5 = 5