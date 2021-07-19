# ------------------------------------------
# DESCRIPTION OF MODULE
# ------------------------------------------

"""
CamPong Score class

It stores the score of a bat and may be used to display the
corresponding text on the screen
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
# CLASSES DEFINITIONS
# ------------------------------------------

class Score(pygame.sprite.Sprite):
    """
    Attributes:
        - font:Font
        - text:String
        - image:Surface
        - rect:Rect. Determines position and hitbox
        - position:(Int,Int). (X,Y)
        - area:Rect. Screen the object is moving across
        - sprite:Sprite
    Methods: __init__, update, calcnewpos
    """
    
    TEXT_SIZE = 20

    def __init__(self, position_init):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 36)
        self.text = "0 - 0"
        # image (appearance)
        self.image = self.font.render(self.text, True, COLOUR_WHITE)
        # rect (hitbox)
        self.rect = self.image.get_rect()
        self.position = position_init
        self.rect.center = self.position
        pygame.draw.rect(self.image, COLOUR_WHITE, self.rect)
        # area that contains the text (i.e. the board itself)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # sprite
        self.sprite = pygame.sprite.RenderPlain(self)

    def update(self, score1, score2, screen, background):
        self.text = str(score1) + " - " + str(score2)
        self.image = self.font.render(self.text, True, COLOUR_WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        screen.blit(background, self.rect, self.rect)
        self.sprite.draw(screen)

    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return rect.move(dx,dy)

