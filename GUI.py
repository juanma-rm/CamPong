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
    import sys
    import os
    import pygame
    import pygame.locals
    import pygame.time
    import math
    from Constants import *
    import Mobile_Object
    import Ball
    import Bat
    import Score
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

def decode_events():

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pass
            # TODO: SEND EXIT EVENT TO MAIN
    # Keyboard
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

def new_score(player_score_nb, screen, background, ball, bat1, bat2, scoresprite):
    if (player_score_nb == 1):
        bat1.score += 1
    elif (player_score_nb == 2):
        bat2.score += 1
    screen.blit(background, (0, 0))        
    ball.reinit(screen, background)
    bat1.reinit(screen, background)
    bat2.reinit(screen, background)
    scoresprite.update(bat1.score, bat2.score)
    scoresprite.draw(screen)
    pygame.display.flip()
    pygame.time.wait(1000)

# ------------------------------------------
# MAIN FLOW
# ------------------------------------------

def gui_pong():

    clock = pygame.time.Clock()
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('CamPong')
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BACKG_COL)
    # Scores and text
    score = Score.Score((SCREEN_W/2, round(SCREEN_H*2/100)))
    scoresprite = pygame.sprite.RenderPlain(score)
    # Create mobile objects
    mob_objs_dic = {}
        # Ball 
    ball = Ball.Ball(speed_angle_init=math.pi/4)
    mob_objs_dic[BALL_ID] = ball
        # Two bats
    bat1 = Bat.Bat(pos_init=1)
    mob_objs_dic[BAT1_ID] = bat1
    bat2 = Bat.Bat(pos_init=2)
    mob_objs_dic[BAT2_ID] = bat2
    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.time.delay(1000)

    # GUI elements updated in loop
    while 1:
        bat_events = decode_events()
        # Background
        screen.blit(background, (0, 0))
        # Ball
        score_ret = ball.update(screen,background,mob_objs_dic)
        # Bats
        bat1.update(screen,background,mob_objs_dic,bat_events[0])
        bat2.update(screen,background,mob_objs_dic,bat_events[1])
        # Score
        screen.blit(background, score.rect, score.rect)
        if (score_ret != 0):    # Some player got a score
            new_score(score_ret, screen, background, ball, bat1, bat2, scoresprite)
        scoresprite.update(bat1.score, bat2.score)
        scoresprite.draw(screen)
        # Other operations
        pygame.display.flip()
        clock.tick(FPS)