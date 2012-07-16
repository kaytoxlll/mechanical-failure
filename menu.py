# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

import pygame
from pygame.locals import *
from constants import *

class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BOXSIZE, BOXSIZE))
        self.name = text
        textSurface = FONT.render(text, True, WHITE, BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        pygame.draw.rect(self.image, WHITE, self.rect, 5)
        self.image.blit(textSurface, self.image.center)

def dialogue(screen, text, choice=False):
    """Prints the text on the screen, along with 'yes' and 'no'
    if there is a choice, else 'continue' button.
    Dialogue covers the lower part of the screen.
    Returns True if the user selected 'yes', else False for 'no'.
    'continue' returns True
    """
    #backup = screen.copy()
    # create each box
    bigbox = pygame.Surface((CENTERWIDTH, CENTERHEIGHT/2,))
    bigboxrect = bigboxrect.get_rect()
    bigboxrect.topleft = (CENTERWIDTH, CENTERHEIGHT/2)
    pygame.draw.rect(bigbox, WHITE, bigboxrect, 10)

    message = font.render(text, True, white, black)
    messagerect = message.get_rect()
    messagerect.topleft = (CENTERWIDTH+TILESIZE, CENTERHEIGHT/2+TILESIZE)

    yesbox = None
    nobox = None
    if choice:
        yesbox = Button("YES", (CENTERXEND-TILESIZE*3, CENTERHEIGHT/2+TILESIZE))
        nobox = Button("NO", (CENTERXEND-TILESIZE*3, CENTERHEIGHT/2+TILESIZE*3))
    else:
        yesbox = Button("NEXT", (CENTERXEND-TILESIZE*3, CENTERHEIGHT/2+TILESIZE))

    screen.blit(bigbox, bigboxrect)
    screen.blit(message, messagerect)
    screen.blit(yesbox.image, yesbox.rect)
    screen.blit(yesbox.image, yesbox.rect)

    while True:
        # handle game events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if yesbox.rect.collidepoint(x, y):
                    #screen.blit(backup, backup.rect)
                    return True
                elif nobox is not None and nobox.rect.collidepoint(x, y):
                    #screen.blit(backup, backup.rect)
                    return False
