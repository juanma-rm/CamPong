# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

# CamPong Score class


# ------------------------------------------
# IMPORTS
# ------------------------------------------

try:

    import pygame
    import pygame.locals
    # from pygame.locals import *
    import pygame.time
    import math
    import random
    import getopt
    from socket import *

    from Constants import *
    
except ImportError as err:
    print ("Error: couldn't load module" + str(err) + ". Exiting...")
    exit()

# ------------------------------------------
# CLASSES DEFINITIONS
# ------------------------------------------

class Score(pygame.sprite.Sprite):
    """
    TODO
    Returns: 
    Functions:  ... TODO
    Attributes:  ... TODO
    """
    
    TEXT_SIZE = 20

    def __init__(self, position_init):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 36)
        self.text = "0 - 0"
        # image (appearance)
        self.image = self.font.render(self.text, True, COLOUR_WHITE)
        # self.image = pygame.Surface((10*self.TEXT_SIZE, 2*self.TEXT_SIZE))
        # rect (hitbox)
        self.rect = self.image.get_rect()
        self.position = position_init
        self.rect.center = self.position
        pygame.draw.rect(self.image, COLOUR_WHITE, self.rect)
        # area that contains the text (i.e. the board itself)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()


    def update(self, score1, score2):
        self.text = str(score1) + " - " + str(score2)
        self.image = self.font.render(self.text, True, COLOUR_WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return rect.move(dx,dy)

