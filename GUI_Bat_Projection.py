# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

"""
CamPong Bat_Projection class

Represents the projection of the object that user is carrying
in front of the camera to move the bat

It is represented by a rectangle
"""

# ------------------------------------------
# IMPORTS
# ------------------------------------------

try:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    import pygame.locals
    from Constants import *
except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# CONSTANTS
# ------------------------------------------

# Init state
HEIGHT_DEFAULT = 30
WIDTH_DEFAULT = 30
COLOUR_DEFAULT = COLOUR_WHITE

# ------------------------------------------
# CLASSES DEFINITIONS
# ------------------------------------------

class Bat_Projection(pygame.sprite.Sprite):
    """
    Attributes:
        - image:Surface
        - rect:Rect. Determines position
        - area:Rect. Screen the object is moving across
        - pos_init:(Int,Int). (X,Y)
        - sprite:Sprite
    Methods: __init__, update
    """
    
    def __init__(self, width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT, colour=COLOUR_DEFAULT):
        # sprite's constructor
        pygame.sprite.Sprite.__init__(self)
        # image (appearance) and rect (hitbox)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, colour, self.rect)
        # area that contains the object (i.e. the board itself)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # initial position
        self.pos_init = self.area.center
        self.rect.center = self.pos_init
        # sprite
        self.sprite = pygame.sprite.RenderPlain(self)

    def update(self, screen, background, x, y):
        # Move the object to a new position (x,y)
        if (screen != None and background != None):
            self.rect.center = (x,y)
            screen.blit(background, self.rect, self.rect)
            self.sprite.draw(screen)
