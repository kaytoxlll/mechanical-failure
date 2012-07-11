# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

import sys
from constants import *
from sprites import *
from images import *
import pygame

# testing
from os.path import join

"""
this is very out of date and will likely have bits of its code
salvages, then this file will be thrown away and replaced with something
with a more descriptive name for the file to execute, like "playgame.py".
"""

# initialization
images = loadAllImages()
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Mechanical Failure")
tile = images["terrain" + "boards"]
pygame.display.set_icon(images["misc" + "logo"])
ground = pygame.Surface((CENTERWIDTH, CENTERHEIGHT))

# music
songPlay("town.mp3")

def drawground(surface, image):
    x= CENTERXSTART
    y= CENTERYSTART
    xinc = image.get_width()
    yinc = image.get_height()
    while y < CENTERYEND:
        while x < CENTERXEND:
            surface.blit(image, (x,y))
            x += xinc
        y += yinc
        x=CENTERXSTART

# set up variables
solidGroup = pygame.sprite.Group()
characterGroup = pygame.sprite.Group()
mapGroup = pygame.sprite.Group()
npcGroup = pygame.sprite.Group()
# set up pc
hero = PC("Cole", images, CENTERCENTER, pygame.sprite.Group(), 100, 0)
characterGroup.add(hero)
# set up map obstacles
newpos = (CENTERCENTER[0] - 100, CENTERCENTER[1] - 100)
barrel = Obstacle("barrel", "terrain", images, newpos, True)
newpos = (CENTERCENTER[0] + 100, CENTERCENTER[1] - 100)
barrel2 = Obstacle("barrel", "terrain", images, newpos, True)
newpos = (CENTERCENTER[0] - 100, CENTERCENTER[1] + 100)
barrel3 = Obstacle("barrel", "terrain", images, newpos, True)
mapGroup.add(barrel, barrel2, barrel3)
# set up npc
newpos = (CENTERCENTER[0] + 100, CENTERCENTER[1] + 100)
rat = NPC("Ratty", "rat", images, newpos, solidGroup)
npcGroup.add(rat)
# set up groups
characterGroup.add(npcGroup)
solidGroup.add(mapGroup)
solidGroup.add(characterGroup)
solidGroup.add(npcGroup)

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

    # update the sprites
    hero.update(solidGroup)
    npcGroup.update(solidGroup)

    # update the screen
    drawground(window, tile)
    solidGroup.draw(window)
    pygame.display.update()
    clock.tick(FPS)
