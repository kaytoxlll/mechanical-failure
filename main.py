# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

import sys
from constants import *
from globalvars import *
from sprites import *
from pc import *
from monsters import *
from menu import *
import pygame

# initialization
pygame.mixer.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Mechanical Failure")
tile = images["terrain" + "stone"]
pygame.display.set_icon(images["misc" + "logo"])
ground = pygame.Surface((CENTERWIDTH, CENTERHEIGHT))

# music
songPlay("industrial.mp3")

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
backgroundGroup = pygame.sprite.Group()
mapGroup = pygame.sprite.Group()
attackGroup = pygame.sprite.Group()
npcGroup = pygame.sprite.Group()
# set up pc
#hero = PC("Cole", CENTERCENTER)
# set up map obstacles
newpos = (CENTERX-TILESIZE*3, CENTERYSTART)
house = Obstacle("house1", "terrain", newpos, True)
newpos = (CENTERCENTER[0] + 100, CENTERCENTER[1] - 100)
barrel = Obstacle("barrel", "terrain", newpos, True)
newpos = (CENTERCENTER[0] - 100, CENTERCENTER[1] + 100)
barrel2 = Obstacle("barrel", "terrain", newpos, True)
mapGroup.add(barrel, barrel2, house)
# set up npc
newpos = (CENTERCENTER[0] + 100, CENTERCENTER[1] + 100)
rat = Rat(newpos)
newpos = (CENTERCENTER[0]+200, CENTERCENTER[1]+ 200)
rat2 = Rat(newpos)
newpos = (CENTERCENTER[0]-200, CENTERCENTER[1]-150)
rat3 = Rat(newpos)
# set up groups
#npcGroup.add(rat, rat2, rat3)
solidGroup.add(mapGroup)
solidGroup.add(hero)
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
            if event.key == K_RETURN:
                print dialogue(window, "This is a dialogue test...")
                print dialogue(window, "Please kill the rats, they bother me")
                print dialogue(window, "will you kill them?")

    # update the sprites
    hero.update()
    npcGroup.update()
    attackGroup.update()

    # update the groups from the queues
    solidGroup.add(solidQ)
    backgroundGroup.add(backgroundQ)
    attackGroup.add(attackQ)
    solidGroup.add(attackQ)
    solidQ.empty()
    backgroundQ.empty()
    attackQ.empty()

    # update the screen
    drawground(window, tile)
    backgroundGroup.draw(window)
    solidGroup.draw(window)
    pygame.display.update()
    clock.tick(FPS)
