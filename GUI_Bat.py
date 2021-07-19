# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

"""
Bat class

Inherits from Mobile_Object
    - The image is a rectangle
    - Init, update and detect_other_obj_hit methods are overriden

Bats can only move in vertical Y axis
Collisions:
    - Top or bottom boundaries: saturates Y coordinate 
    - Bat: call to ball bounce
"""

# ------------------------------------------
# IMPORTS
# ------------------------------------------

try:
    from Constants import *
    import GUI_Mobile_Object as mo
except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# CONSTANTS
# ------------------------------------------

HEIGHT_DEFAULT_BAT = 100
WIDTH_DEFAULT_BAT = 15
SPEED_ANG_DEFAULT_BAT = 0
SPEED_MOD_DEFAULT_BAT = 10
COLOUR_DEFAULT_BAT = COLOUR_WHITE

# ------------------------------------------
# CLASSES DEFINITIONS
# ------------------------------------------

class Bat(mo.Mobile_Object):
    """
    Attributes:
        - Same as for GUI_Mobile_Object
    Methods:
        - __init__, update and detect_other_obj_hit methods are overriden
    """
    def __init__(self, height=HEIGHT_DEFAULT_BAT, width=WIDTH_DEFAULT_BAT,
            pos_init=None, colour=mo.COLOUR_DEFAULT,
            speed_angle_init=SPEED_ANG_DEFAULT_BAT, speed_mod_init=SPEED_MOD_DEFAULT_BAT):

        # sprite's constructor
        pygame.sprite.Sprite.__init__(self)
        # image (appearance) and rect (hitbox)
        self.image = pygame.Surface((width, height))
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
        if (self.pos_init == None):    # By default: bat in left side
            self.pos_init = (width, self.area.centery)
        elif (self.pos_init == 1):     # Bat1 (left)
            self.pos_init = (width, self.area.centery)
        elif (self.pos_init == 2):     # Bat2 (right)
            self.pos_init = (self.area.right-width, self.area.centery)
        # initial speed
        self.speed_angle_init = speed_angle_init
        self.speed_mod_init = speed_mod_init
        self.speed_mod_step = min(self.rect.width,self.rect.height)/2
        self.reinit()
        # sprite
        self.sprite = pygame.sprite.RenderPlain(self)
        # score
        self.score = 0

    def update(self, screen, background, mob_objs_dic, dir):
        # Implements specific collision management for bat object.
        
        # Init state
        speed_to_consume = self.vector[1]
        keep_moving = True
        if (dir == BAT_GO_UP_ID):       # go up
            self.vector = (PI/2, self.speed_mod_init)    
        elif (dir == BAT_GO_DOWN_ID):   # go down
            self.vector = (-PI/2, self.speed_mod_init)
        else:
            keep_moving = False
            screen.blit(background, self.rect, self.rect)
            self.sprite.draw(screen)
        # While there are speed steps to consume or not critical collisions, keep moving
        while (speed_to_consume > 0 and keep_moving):
            collisions = self.update_step(speed_to_consume, mob_objs_dic)
            if (len(collisions) == 0):      # No collision
                self.rect = self.rect_next      # Ball keeps its previous trajectory
            else:                           # Collisions: attend them
                for collision in collisions:    # 
                    # Check if there have been collisions with borders
                    if (collision[0] == COLLISION_BOUND_LEFT_ID):       # Should not happen
                        keep_moving = False
                        self.reinit()
                    elif (collision[0] == COLLISION_BOUND_RIGHT_ID):    # Should not happen
                        keep_moving = False
                        self.reinit()
                    elif (collision[0] == COLLISION_BOUND_TOP_ID):
                        # Saturate vertical coordinate (top) to fit into the board
                        self.rect.top = self.area.top
                    elif (collision[0] == COLLISION_BOUND_BOT_ID):
                        # Saturate vertical coordinate (bottom) to fit into the board
                        self.rect.bottom = self.area.bottom
                    # Check other collisions
                    elif (collision[0] == BALL_ID):
                        mob_objs_dic[BALL_ID].bounce(BALL_VERT_BOUNCE, collision[1])

            screen.blit(background, self.rect, self.rect)
            self.sprite.draw(screen)
            speed_to_consume -= self.speed_mod_step         # Part of the speed is consumed
        
    def detect_other_obj_hit(self, mob_objs_dic):
        # Returns collisions returned by ball's detect_other_obj_hit implementation
        # To improve this: it would be better to have a common function (defined in some common file)
        # instead of a method in ball called from bat
        return mob_objs_dic[BALL_ID].detect_other_obj_hit(mob_objs_dic)