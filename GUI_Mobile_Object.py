# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

"""
Mobile_Object class

Represents mobile objects which consist of:
  - A rect (for position and collisions)
  - A speed vector (angle, module)
  - A screen to the one they move across
  - Several methods to be moved, to check collisions, ...

Regarding position update methods, step to step procedure is used to
avoid tunneling and other weird behaviours. This way, the object is 
able to move fast (in comparison to its size) without misbehaving. 

Inherits from Sprite (pygame)

Axis: X (positive to the right), Y (positive to the bottom)
"""

# ------------------------------------------
# IMPORTS
# ------------------------------------------

try:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    import math
    from Constants import *
except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# CONSTANTS
# ------------------------------------------

# Init state
HEIGHT_DEFAULT = 10
WIDTH_DEFAULT = 10
SPEED_ANG_DEFAULT = 0
SPEED_MOD_DEFAULT = 12
COLOUR_DEFAULT = COLOUR_WHITE

# ------------------------------------------
# CLASSES DEFINITIONS
# ------------------------------------------

class Mobile_Object(pygame.sprite.Sprite):
    """
    Attributes:
        - image:Surface
        - rect:Rect. Determines position and hitbox
        - rect_next:Rect. Next position of the object
        - area:Rect. Screen the object is moving across
        - vector:(Float,Int). (speed angle, speed module)
        - pos_init:(Int,Int). (X,Y)
        - speed_angle_init:Float. Range [-pi,pi]
        - speed_mod_init:Int. Total pixels that the object moves per frame
        - speed_mod_step:Int. Pixels that the object moves each step within a frame
        - sprite:Sprite
    Methods: __init__, reinit, update_step, update, calc_new_pos_step, calc_new_pos,
        check_collisions, detect_boundary_hit, detect_other_obj_hit
    """

    def __init__(self, height=HEIGHT_DEFAULT, width=WIDTH_DEFAULT, 
                colour=COLOUR_DEFAULT, pos_init=None,
                speed_angle_init=SPEED_ANG_DEFAULT, speed_mod_init=SPEED_MOD_DEFAULT):
        # sprite's constructor
        pygame.sprite.Sprite.__init__(self)
        # image (appearance) and rect (hitbox)
        self.image = pygame.Surface((height, width))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, colour, self.rect)
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
        # obj is moved step-by-step in steps that take each less of the half of the
        # minimum dimension of the object. This way, tunelling problems are avoided
        # (e.g. the object is so fast that goes out of two closer bounds, cross other
        #  objects, ...). For each step, collisions are checked
        self.speed_mod_step = min(self.rect.width,self.rect.height)/2
        # sprite
        self.sprite = pygame.sprite.RenderPlain(self)
        self.reinit()
    
    def reinit(self, screen=None, background=None):
        # Initializes the object position and speed to the init values
        self.rect.center = self.pos_init
        self.vector = (self.speed_angle_init, self.speed_mod_init)
        self.rect_next.center = self.rect.center
        if (screen != None and background != None):
            screen.blit(background, self.rect, self.rect)
            self.sprite.draw(screen)

    def update_step(self,speed_to_consume, mob_objs_dic):
        # Determine next position of the object when moving at speed_mod_step and
        # returns a list containing the collisions that took place
        self.rect_next = self.calc_new_pos_step(speed_to_consume)
        collisions = self.check_collisions(mob_objs_dic)
        return collisions

    def update(self, screen, background, mob_objs_dic):
        # Move the object the amount of pixels determined by speed (vector) going 
        # step by step. For each little step, collisions are checked and attended.
        # If some collision is supossed to finish the move of the object, 
        # keep_moving will switch to False. Otherwise, the object will move up to
        # consume all the speed intended to.
        
        speed_to_consume = self.vector[1]
        keep_moving = True
        # While there are speed steps to consume or not critical collisions, keep moving
        while (speed_to_consume > 0 and keep_moving):
            collisions = self.update_step(speed_to_consume, mob_objs_dic)
            if (len(collisions) == 0):      # No collision
                # Move and draw object by its original trajectory
                self.rect = self.rect_next      
                screen.blit(background, self.rect, self.rect)
                self.sprite.draw(screen)
            else:                           # Attend collisions
                pass                            # Each children class should implement its 
                                                # own collision procedure
            speed_to_consume -= self.speed_mod_step # Part of the speed is consumed
            
    def calc_new_pos_step(self, calc_new_pos_step):
        # Returns the new position the object would be at after moving its rect what vector determines
        # This function goes step by step (at speed_mod_step) checking collisions
        (angle,z) = self.vector
        (dx,dy) = (round(calc_new_pos_step*math.cos(angle)),round(calc_new_pos_step*math.sin(angle)))
        return self.rect.move(dx,-dy) # rect.move works with angle > 0 in clock wise

    def calc_new_pos(self):
        # Returns the new position the object would be at after moving its rect what vector determines
        # This function does not go step by step
        (angle,z) = self.vector
        (dx,dy) = (round(z*math.cos(angle)),round(z*math.sin(angle))) 
        return self.rect.move(dx,-dy) # rect.move works with angle > 0 in clock wise

    def check_collisions(self, mob_objs_dic):
        # For each object stored in mob_objs_dic and for each boundary, the possible collisions
        # taking place are analysed. In case of collision, this is added to collisions list which
        # will be returned
        collisions = [] # list of collisions, being each collision: (collision_id, collision_side)
                        # collision_id identifies the object that the current object collides with
                        # collision_side identifies the side of the current object that has been collided
        # Check boundary collisions
        collisions_bound = self.detect_boundary_hit()
        for collision in collisions_bound:
            collisions.append(collision)
        # Check mobile obj collisions
        collisions_mob_obj = self.detect_other_obj_hit(mob_objs_dic)
        for collision in collisions_mob_obj:
            collisions.append(collision)
        return collisions
    
    def detect_boundary_hit(self):
        # Returns a list of boundaries that the obj is colliding with
        collisions = []
        # Analyse each corner of the object to check whether this is within the boundaries
        tl = not self.area.collidepoint(self.rect_next.topleft)
        tr = not self.area.collidepoint(self.rect_next.topright)
        bl = not self.area.collidepoint(self.rect_next.bottomleft)
        br = not self.area.collidepoint(self.rect_next.bottomright)
        if (tl == True and tr == True):   # Hits top
            collisions.append((COLLISION_BOUND_TOP_ID,COLLISION_TOP))
        if (bl == True and br == True):   # Hits bottom
            collisions.append((COLLISION_BOUND_BOT_ID,COLLISION_BOT))
        if (tl == True and bl == True):   # Hits left
            collisions.append((COLLISION_BOUND_LEFT_ID,COLLISION_LEFT))
        if (tr == True and br == True):   # Hits right
            collisions.append((COLLISION_BOUND_RIGHT_ID,COLLISION_RIGHT))
        return collisions

    def detect_other_obj_hit(self, mob_objs_dic):
        # Returns a list of elements that the obj is colliding with
        collisions = []
        for mob_obj_key in mob_objs_dic:
            mob_obj = mob_objs_dic[mob_obj_key]
            if (mob_obj != self and self.rect.colliderect(mob_obj)):
                collisions.append((mob_obj_key,0))
        return collisions