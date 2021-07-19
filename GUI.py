# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

"""
CamPong GUI module

Takes charge of creating and handling the graphical elements and scores
Elements:
    - Screen
    - Bat1: left
    - Bat2: right
    - Ball
    - Score text
"""

# ------------------------------------------
# IMPORTS
# ------------------------------------------

try:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    import pygame.locals
    import pygame.time
    import math
    from Constants import *
    import GUI_Mobile_Object
    import GUI_Ball
    import GUI_Bat
    import GUI_Score
    import Keyboard
    import IA
    import Cam
    import GUI_Bat_Projection
except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# GLOBAL CONSTANTS
# ------------------------------------------


# ------------------------------------------
# GLOBAL VARIABLES
# ------------------------------------------



# ------------------------------------------
# FUNCTIONS DEFINITIONS
# ------------------------------------------

def decode_misc_events():

    exit = False
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            exit = True
    return exit


def new_score(player_score_nb, bat1, bat2):
    if (player_score_nb == SCORE_BAT1):
        bat1.score += 1
    elif (player_score_nb == SCORE_BAT2):
        bat2.score += 1

def new_ball(screen, background, ball, bat1, bat2, score):
    screen.blit(background, (0, 0))        
    ball.reinit(screen, background)
    bat1.reinit(screen, background)
    bat2.reinit(screen, background)
    score.update(bat1.score, bat2.score, screen, background)
    pygame.display.flip()
    pygame.time.wait(1)

def get_cam_events(bat, proj_y):
    bat_event = BAT_STILL
    if ( proj_y - bat.rect.centery > CAM_OFFSET_SHAK ):
        bat_event = BAT_GO_DOWN_ID
    elif ( proj_y - bat.rect.centery < -CAM_OFFSET_SHAK):
        bat_event = BAT_GO_UP_ID
    return bat_event

# ------------------------------------------
# MAIN FLOW
# ------------------------------------------

def gui_pong(t0_exit, t1_queue, nb_players=NB_PLAYERS_DEF, player_control=CONTROLLER_DEF):

    clock = pygame.time.Clock()
    prev_time_ms = 0
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('CamPong')
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BACKG_COL)
    # Nb of players and type of control
    if (nb_players == 2):
        bat1_controller = player_control
        bat2_controller = player_control
    elif (nb_players == 1):
        bat1_controller = player_control
        bat2_controller = CONTROLLER_IA
    elif (nb_players == 0):
        bat1_controller = CONTROLLER_IA
        bat2_controller = CONTROLLER_IA

    # Scores and text
    score = GUI_Score.Score((SCREEN_W/2, round(SCREEN_H*2/100)))
    # Create mobile objects
    mob_objs_dic = {}
        # Ball 
    ball = GUI_Ball.Ball(speed_angle_init=math.pi/4)
    mob_objs_dic[BALL_ID] = ball
        # Two bats
    bat1 = GUI_Bat.Bat(pos_init=1)
    mob_objs_dic[BAT1_ID] = bat1
    bat2 = GUI_Bat.Bat(pos_init=2)
    mob_objs_dic[BAT2_ID] = bat2
    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.time.delay(1000)
    # Pointers (position of circles detected by cam)
    if (bat1_controller == CONTROLLER_CAM):
        bat1_pointer = GUI_Bat_Projection.Bat_Projection(colour=COLOUR_RED)
    if (bat2_controller == CONTROLLER_CAM):
        bat2_pointer = GUI_Bat_Projection.Bat_Projection(colour=COLOUR_GREEN)

    # Cam (temperary here)
    Cam.cam_init()

    # GUI elements updated in loop
    while(1):

        # Check errors
        if (decode_misc_events() == True):
            t0_exit.put((EXIT_SUC, ""))

        # Background
        screen.blit(background, (0, 0))

        # Bat events
        bat1_events = None
        bat2_events = None
        key_events = Keyboard.get_key_events()   # Keyboard
        # Get positions from cam if necessary
        if (player_control == CONTROLLER_CAM):
            while (not t1_queue.empty()):
                (bat1_x, bat1_y, bat2_x, bat2_y, state) = t1_queue.get()
        # Get events from the corresponding controller / IA
        if (bat1_controller == CONTROLLER_KEYB):
            bat1_events = key_events[0]
        elif (bat1_controller == CONTROLLER_IA):
            bat1_events = IA.ia_get_event(bat1,BAT1_ID,ball)
        elif (bat1_controller == CONTROLLER_CAM):
            if (bat1_x != None or bat1_y != None):
                bat1_events = get_cam_events(bat1, bat1_y)
                bat1_pointer.update(screen, background, bat1_x, bat1_y)
        if (bat2_controller == CONTROLLER_KEYB):
            bat2_events = key_events[1]
        elif (bat2_controller == CONTROLLER_IA):
            bat2_events = IA.ia_get_event(bat2,BAT2_ID,ball)
        elif (bat2_controller == CONTROLLER_CAM):
            if (bat2_x != None or bat2_y != None):
                bat2_events = get_cam_events(bat2, bat2_y)
                bat2_pointer.update(screen, background, bat2_x, bat2_y)

        # Ball
        score_ret = ball.update(screen,background,mob_objs_dic)
        # Bats
        bat1.update(screen,background,mob_objs_dic,bat1_events)
        bat2.update(screen,background,mob_objs_dic,bat2_events)
        # Score
        screen.blit(background, score.rect, score.rect)
        if (score_ret != SCORE_NONE):    # Some player got a score
            new_score(score_ret, bat1, bat2)
            new_ball(screen, background, ball, bat1, bat2, score)
        else:
            score.update(bat1.score, bat2.score, screen, background)
            
        # Other operations
        pygame.display.flip()
        # Timing 
        clock.tick(FPS)
        if (SHOW_REAL_FPS):
            real_fps = int(1000 / (pygame.time.get_ticks() - prev_time_ms))
            print("GUI fps: " + str(real_fps))
        prev_time_ms = pygame.time.get_ticks()