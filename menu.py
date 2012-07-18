# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

import sys
import pygame
from pygame.locals import *
from constants import *

class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BOXSIZE, BOXSIZE-TILESIZE))
        self.name = text
        textSurface = FONT.render(text, True, WHITE, BLACK)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, WHITE, self.rect, 5)
        (x,y) = self.rect.center
        x -= textSurface.get_width()/2
        y -= textSurface.get_height()/2
        self.image.blit(textSurface, (x,y))
        self.rect.topleft = pos

def dialogue(screen, text):
    """Prints the text on the screen, along with buttons.
    If the text ends with a "?", then they options are 'yes' and 'no'
    If the text is not a question, button is 'next'
    Returns True for 'yes' and 'next', False for 'no'
    """
    choice = False
    if text[-1] == "?":
        choice = True
    # create each box
    bigbox = pygame.Surface((CENTERWIDTH, CENTERHEIGHT/2,))
    bigboxrect = bigbox.get_rect()
    pygame.draw.rect(bigbox, WHITE, bigboxrect, 10)
    bigboxrect.topleft = (CENTERXSTART, CENTERHEIGHT/2)

    message = FONT.render(text, True, WHITE, BLACK)
    messagerect = message.get_rect()
    messagerect.topleft = (CENTERXSTART+TILESIZE, CENTERHEIGHT/2+TILESIZE)

    yesbox = None
    nobox = None
    choicebox = None
    if not choice:
        nextbox = Button("NEXT", (CENTERXSTART+TILESIZE, CENTERYEND-BOXSIZE))
    else:
        yesbox = Button("YES", (CENTERXSTART+BOXSIZE+TILESIZE*2, CENTERYEND-BOXSIZE))
        nobox = Button("NO", (CENTERXSTART+BOXSIZE*2+TILESIZE*3, CENTERYEND-BOXSIZE))

    screen.blit(bigbox, bigboxrect)
    screen.blit(message, messagerect)
    buttons = pygame.sprite.Group()
    if choice:
        buttons.add(nobox, yesbox)
    else:
        buttons.add(nextbox)
    buttons.draw(screen)
    pygame.display.update()

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
                if choice:
                    if yesbox.rect.collidepoint(x, y):
                        return True
                    elif nobox.rect.collidepoint(x, y):
                        return False
                elif nextbox.rect.collidepoint(x,y):
                    return True