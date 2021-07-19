# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

"""
IA module

Takes charge of calculating the events (up/down) for IA
The strategy is as follows:
    - If the ball is in oponent's court: bat goes back to 
    vertical center
    - If the ball is in IA's court: bat approachs the ball 
    by comparing ball vertical center to bat one
    - Moreover, a random factor is used to make the move more
    natural and an offset is used to avoid bat' shaking
"""

# ------------------------------------------
# IMPORTS
# ------------------------------------------

try:
    import random
    from Constants import *
except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# GLOBAL VARIABLES
# ------------------------------------------

bat1_prev_ball_side = 0
bat2_prev_ball_side = 0
bat1_random_offset = 0
bat2_random_offset = 0

# ------------------------------------------
# FUNCTIONS DEFINITIONS
# ------------------------------------------

def ia_get_event(bat, bat_id, ball):
    # Takes a bat and the ball to calculate IA's bat next position.
    # bat:Bat: IA's bat 
    # ball:Ball
    # bat_id(Int): identifies the bat
    # Returns event_ret:Int: identifies the event for bat to do

    event_ret = BAT_STILL   # Do not move by default

    # Each time the ball changes of court, a new random is generated
    # in order to make the IA's move more wide ranging. While the
    # ball has not changed of court, previous offset is used

    # Check whether the ball has changed of side
    global bat1_prev_ball_side
    global bat2_prev_ball_side
    global bat1_random_offset
    global bat2_random_offset
    prev_ball_side = 0
    random_offset = 0
    if (bat_id == BAT1_ID):
        prev_ball_side = bat1_prev_ball_side
        random_offset = bat1_random_offset
    elif (bat_id == BAT2_ID):
        prev_ball_side = bat2_prev_ball_side
        random_offset = bat2_random_offset
    new_ball_side = BAT1_ID if (abs(ball.rect.centerx-ball.area.centerx) > ball.rect.width) else BAT2_ID
    if (prev_ball_side == 0 or prev_ball_side != new_ball_side):  # New ball starting or ball has changed of side
        prev_ball_side = new_ball_side
        random_offset = IA_OFFSET*(random.random())
        if (bat_id == BAT1_ID):
            bat1_prev_ball_side = prev_ball_side
            bat1_random_offset = random_offset
        elif (bat_id == BAT2_ID):
            bat2_prev_ball_side = prev_ball_side
            bat2_random_offset = random_offset

    # Ball in opposite area -> come back to center
    if ( abs(ball.rect.centerx-bat.rect.centerx) > bat.area.width/2 ):
        
        if (bat.rect.centery-bat.area.centery > (random_offset)):       # Bat below the ball
            event_ret = BAT_GO_UP_ID    # go up
        elif (bat.rect.centery-bat.area.centery < -(random_offset)):    # Bat above the ball
            event_ret = BAT_GO_DOWN_ID  # go down
        else:
            event_ret = BAT_STILL
    # Ball in own area -> predict ball Y coordinate
    else:
        if (ball.rect.centery-bat.rect.centery > (random_offset)):      # Bat below the ball
            event_ret = BAT_GO_DOWN_ID    # go down 
        elif (ball.rect.centery-bat.rect.centery < -(random_offset)):   # Bat above the ball
            event_ret = BAT_GO_UP_ID        # go up
        else:
            event_ret = BAT_STILL

    return event_ret
