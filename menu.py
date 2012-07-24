# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

import sys
import pygame
import sprites
from pygame.locals import *
from constants import *
import globalvars

pygame.init()

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

def draw_hud():
    """Draw the hero's stats to the side of the screen."""
    # blank screen
    rect = pygame.Rect((LBORDERXSTART, BORDERYSTART), (BORDERWIDTH, BORDERHEIGHT))
    globalvars.window.fill(BLACK, rect)
    rect.topleft = (RBORDERXSTART, BORDERYSTART)
    globalvars.window.fill(BLACK, rect)
    x = LBORDERXSTART + TILESIZE
    y = BORDERYSTART + TILESIZE
    # draw player stats to left hud
    hudlist = []
    hudlist.append(globalvars.hero.name + "'s stats:")
    hudlist.append("HP:      " + str(globalvars.hero.hp)+" / "+ str(globalvars.hero.hpmax))
    hudlist.append("Coins:   " + str(globalvars.hero.coins))
    hudlist.append("Bullets: " + str(globalvars.hero.ammo))
    hudlist.append("Potions: " + str(globalvars.hero.potions))
    hudlist.append("Keys:    " + str(globalvars.hero.keys))
    for i in hudlist:
        textSurface = FONTSMALL.render(i, True, WHITE, BLACK)
        textRect = textSurface.get_rect()
        globalvars.window.blit(textSurface, (x,y))
        y += TILESIZE/2
    # print gameplay instructions
    y += TILESIZE
    guidelist = []
    guidelist.append("Move up:      W")
    guidelist.append("Move left:    A")
    guidelist.append("Move down:    S")
    guidelist.append("Move right:   D")
    guidelist.append("Attack:       Left-click")
    guidelist.append("Shoot:        Right-click")
    guidelist.append("Talk / examine: E")
    guidelist.append("Drink potion: SPACE")
    guidelist.append("Pause:        ENTER")
    guidelist.append("Quit:         ESC")
    for i in guidelist:
        textSurface = FONTSMALL.render(i, True, WHITE, BLACK)
        textRect = textSurface.get_rect()
        globalvars.window.blit(textSurface, (x,y))
        y += TILESIZE
    # draw npc hp to right hud
    x = RBORDERXSTART + TILESIZE
    y = BORDERYSTART + TILESIZE
    hudlist = []
    for s in globalvars.solidGroup:
        if isinstance(s, sprites.NPC) and s is not globalvars.hero:
            hudlist.append(s.name + " hp: " + str(s.hp))
    for i in hudlist:
        textSurface = FONTSMALL.render(i, True, WHITE, BLACK)
        textRect = textSurface.get_rect()
        globalvars.window.blit(textSurface, (x,y))
        y += TILESIZE

def dialogue(text):
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

    globalvars.window.blit(bigbox, bigboxrect)
    globalvars.window.blit(message, messagerect)
    buttons = pygame.sprite.Group()
    if choice:
        buttons.add(nobox, yesbox)
    else:
        buttons.add(nextbox)
    buttons.draw(globalvars.window)
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
                elif event.key == K_RETURN:
                    if not choice:
                        return True
                elif event.key == K_y:
                    if choice:
                        return True
                elif event.key == K_n:
                    if choice:
                        return False
            elif event.type == MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if choice:
                    if yesbox.rect.collidepoint(x, y):
                        return True
                    elif nobox.rect.collidepoint(x, y):
                        return False
                elif nextbox.rect.collidepoint(x,y):
                    return True
