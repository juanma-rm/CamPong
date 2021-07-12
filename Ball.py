# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

"""
Ball class

Inherits from Mobile_Object
    - The image is a circle
    - Init, update and detect_other_obj_hit methods are overriden

Collisions:
    - Top or bottom boundaries: symmetric bounce 
    - Left or right boundaries: score for bat2 or bat1 respectively
    - Bat: symmetric bounce if collides in centre of bat; assymetric
        bounde otherwise
"""

# ------------------------------------------
# IMPORTS
# ------------------------------------------

from hashlib import new


try:
    import pygame
    import pygame.locals
    import pygame.time
    import math
    import random
    from Constants import *
    from Mobile_Object import *
except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# CONSTANTS
# ------------------------------------------

RADIUS_DEFAULT = 11
SPEED_MOD_DEFAULT = 12

# ------------------------------------------
# FUNCTIONS DEFINITIONS
# ------------------------------------------

def gen_random_init_ang_ball():
    # Generate random init angle no vertical
    angle = PI*(-1 + 2*random.random())  # random in [-pi, pi] rad
    while ( ( (abs(angle) > (3/8)*PI) and (abs(angle) < (5/8)*PI) )
            or (abs(angle) < (1/10)*PI) or (abs(angle) > (9/10)*PI) ):
        angle = PI*(-1 + 2*random.random()) # new angle in same range
    return angle

# ------------------------------------------
# CLASSES DEFINITIONS
# ------------------------------------------

class Ball(Mobile_Object):

    def __init__(self, radius=RADIUS_DEFAULT, pos_init=None, colour=COLOUR_DEFAULT,
            speed_angle_init=SPEED_ANG_DEFAULT, speed_mod_init=SPEED_MOD_DEFAULT):

        # sprite's constructor
        pygame.sprite.Sprite.__init__(self)
        # image (appearance) and rect (hitbox)
        self.image = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
            # SRCALPHA allows getting a circle as image
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, colour, (radius, radius), radius, 0)
        self.rect_next = self.image.get_rect()   # rect_next initializes as rect
        # area that contains the object (i.e. the board itself)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # speed
        self.vector = (0,0) # To be initialised in reinit()
        # initial position
        self.pos_init = pos_init
        if (self.pos_init == None):    # By default: position at center of screen
            self.pos_init = self.area.center
        # initial speed
        self.speed_angle_init = speed_angle_init
        self.speed_mod_init = speed_mod_init
        self.speed_mod_step = min(self.rect.width,self.rect.height)/2
        self.reinit()
        # sprite
        self.sprite = pygame.sprite.RenderPlain(self)
           
    def reinit(self, screen=None, background=None):
        # Initializes the object position and speed to the init values (new random angle)
        self.rect.center = self.pos_init
        self.vector = (gen_random_init_ang_ball(), self.speed_mod_init)
        self.rect_next.center = self.rect.center
        if (screen != None and background != None):
            screen.blit(background, self.rect, self.rect)
            self.sprite.draw(screen)
        
    def update(self, screen, background, mob_objs_dic):
        # Implements specific collision management for ball object.
        # Returns score (0 no score, 1 score for bat1, 2 score for bat2)

        # Init state
        speed_to_consume = self.vector[1]
        keep_moving = True
        score = 0
        # While there are speed steps to consume or not critical collisions, keep moving
        while (speed_to_consume > 0 and keep_moving):
            collisions = self.update_step(speed_to_consume, mob_objs_dic)
            if (len(collisions) == 0):      # No collision
                self.rect = self.rect_next      # Ball keeps its previous trajectory
            else:                           # Collisions: attend them
                for collision in collisions:
                    # Check if there have been collisions with borders
                    if (collision[0] == COLLISION_BOUND_LEFT_ID):
                        score = 2
                        keep_moving = False
                    elif (collision[0] == COLLISION_BOUND_RIGHT_ID):
                        score = 1
                        keep_moving = False
                    elif (collision[0] == COLLISION_BOUND_TOP_ID):
                        self.bounce(BALL_HOR_BOUNCE)
                        # Saturate vertical coordinate (top) to fit into the board
                        self.rect.top = self.area.top+1           
                    elif (collision[0] == COLLISION_BOUND_BOT_ID):
                        self.bounce(BALL_HOR_BOUNCE)
                        # Saturate vertical coordinate (bottom) to fit into the board
                        self.rect.bottom = self.area.bottom-1     
                    # Check collisions with other mobile objects
                    elif (collision[0] == BAT1_ID):
                        self.bounce(BALL_VERT_BOUNCE, collision[1])
                        self.rect.right += 10
                    elif (collision[0] == BAT2_ID):
                        self.bounce(BALL_VERT_BOUNCE, collision[1])
                        self.rect.left -= 10

            speed_to_consume -= self.speed_mod_step         # Part of the speed is consumed
            screen.blit(background, self.rect, self.rect)
            self.sprite.draw(screen)

        return score

    # def bounce(self, orientation, bat_height=0):
    #     # Calculates new angle of the ball after hitting an obstacle
    #     (curr_ang, curr_speed) = self.vector
    #     if (orientation == BALL_HOR_BOUNCE):        # ball hits horizontal obstacle
    #         new_ang = -curr_ang
    #     elif (orientation == BALL_VERT_BOUNCE):     # ball hits vertical obstacle (bat)
    #         # First, calculate symmetric angle
    #         if (curr_ang > 0):
    #             new_ang_sym = PI - curr_ang
    #         else:
    #             new_ang_sym = - curr_ang - PI
    #         # Now, the previous angle is modifed according to part of the bat that was hit
    #         if (bat_height == COLLISION_BAT_1_5):
    #             new_ang = new_ang_sym*1.1
    #         elif (bat_height == COLLISION_BAT_2_5):
    #             new_ang = new_ang_sym*1.05
    #         elif (bat_height == COLLISION_BAT_3_5):
    #             new_ang = new_ang_sym*1
    #         elif (bat_height == COLLISION_BAT_4_5):
    #             new_ang = new_ang_sym*0.95
    #         elif (bat_height == COLLISION_BAT_5_5):
    #             new_ang = new_ang_sym*0.9
    #         # Avoid the ball angle to exceed its angle quadrant; e.g. if new_angle_temp was 85º, 
    #         # new_angle should not exceed 90º
    #         if (new_ang_sym < PI/2 and new_ang > 0.90*PI/2):
    #             new_ang = new_ang_sym
    #         elif (new_ang_sym > -PI/2 and new_ang < -0.90*PI/2):
    #             new_ang = new_ang_sym
            
    #     # Do not allow close to vertical angles to make the game funnier
    #     if (new_ang > 0.85*PI/2 and new_ang < PI/2):
    #         new_ang = 0.85*PI/2
    #     elif (new_ang > PI/2 and new_ang < 1.15*PI/2):
    #         new_ang = 1.15*PI/2
    #     elif (new_ang < -0.85*PI/2 and new_ang > -PI/2):
    #         new_ang = -0.85*PI/2
    #     elif (new_ang < -PI/2 and new_ang > -1.15*PI/2):
    #         new_ang = -1.15*PI/2

    #     self.vector = (new_ang,curr_speed)
    
    def bounce(self, orientation, bat_height=0):
        # Calculates new angle of the ball after hitting an obstacle
        (curr_ang, curr_speed) = self.vector
        if (orientation == BALL_HOR_BOUNCE):        # ball hits horizontal obstacle
            new_ang = -curr_ang
        elif (orientation == BALL_VERT_BOUNCE):     # ball hits vertical obstacle (bat)
            # The angle is calculated according to part of the bat that was hit
            if (bat_height == COLLISION_BAT_1_5):
                new_ang = PI/4
            elif (bat_height == COLLISION_BAT_2_5):
                new_ang = PI/8
            elif (bat_height == COLLISION_BAT_3_5):
                new_ang = 0
            elif (bat_height == COLLISION_BAT_4_5):
                new_ang = -PI/8
            elif (bat_height == COLLISION_BAT_5_5):
                new_ang = -PI/4
            # According to previous angle, the ball now will go the previous side
            if (curr_ang > -PI/2 and curr_ang < PI/2):  # ball was going to the right
                new_ang = PI - new_ang
            else:
                new_ang = new_ang
        self.vector = (new_ang,curr_speed)

    def detect_other_obj_hit(self, mob_objs_dic):
        # Returns a list of elements that the ball is colliding with
        collisions = []
        ball = mob_objs_dic[BALL_ID]
        for bat_id in [BAT1_ID, BAT2_ID]:
            bat = mob_objs_dic[bat_id]
            if (ball.rect.colliderect(bat)):
                collision_height = None
                if (ball.rect.centery < (bat.rect.top+(1/5)*bat.rect.height) ):
                    collision_height = COLLISION_BAT_1_5
                elif (ball.rect.centery < (bat.rect.top+(2/5)*bat.rect.height) ):
                    collision_height = COLLISION_BAT_2_5
                elif (ball.rect.centery < (bat.rect.top+(3/5)*bat.rect.height) ):
                    collision_height = COLLISION_BAT_3_5
                elif (ball.rect.centery < (bat.rect.top+(4/5)*bat.rect.height) ):
                    collision_height = COLLISION_BAT_4_5
                # elif (ball.rect.centery > (bat.rect.top+(5/5)*bat.rect.height) ):
                else:
                    collision_height = COLLISION_BAT_5_5
                collisions.append((bat_id,collision_height))
        return collisions


    # def detect_other_obj_hit(self, mob_objs_dic):
    #     # Returns a list of elements that the obj is colliding with
    #     collisions = []
    #     for mob_obj_key in mob_objs_dic:
    #         mob_obj = mob_objs_dic[mob_obj_key]
    #         # Collision with bat1
    #         if (mob_obj_key == BAT1_ID and self.rect.colliderect(mob_obj)):
    #             if (self.)
    #         # Collision with bat2
    #         if (mob_obj_key == BAT2_ID and self.rect.colliderect(mob_obj)):
    #             pass
    #         # if (mob_obj != self and self.rect.colliderect(mob_obj)):
    #         #     collisions.append((mob_obj_key,0))
    #     return collisions