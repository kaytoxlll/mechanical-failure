# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

import sys
from constants import *
from globalvars import *
from world import *
from sprites import *
from pc import *
from monsters import *
from menu import *
import pygame

# initialization
pygame.mixer.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Mechanical Failure")
pygame.display.set_icon(globalvars.images["misc" + "logo"])

# set up groups
world = World()

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
                world.music.pause()
                textSurface = FONT.render("PAUSED", True, WHITE, BLACK)
                rect = textSurface.get_rect()
                rect.center = CENTERCENTER
                globalvars.window.blit(textSurface, rect)
                pygame.display.update()
                paused = True
                while paused:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == KEYDOWN:
                            if event.key == K_RETURN:
                                paused = False
                                world.music.unpause()

    # update the sprites
    moveval = globalvars.hero.update()
    world.update()
    globalvars.attackGroup.update()

    # update the groups from the queues
    globalvars.solidGroup.add(globalvars.solidQ)
    world.currentmap.backgroundGroup.add(globalvars.backgroundQ)
    globalvars.attackGroup.add(globalvars.attackQ)
    globalvars.solidGroup.add(globalvars.attackQ)
    globalvars.solidQ.empty()
    globalvars.backgroundQ.empty()
    globalvars.attackQ.empty()
    globalvars.itemGroup.add(globalvars.itemQ)
    world.currentmap.itemGroup.add(globalvars.itemQ)
    globalvars.itemQ.empty()

    # Update map if hero moved off the edge of the screen
    if moveval == "north" or \
      moveval == "south" or \
      moveval == "east" or \
      moveval == "west" or \
      moveval == "up" or \
      moveval == "down":
        world.load(moveval)

    # update the screen
    draw_hud()
    world.draw(globalvars.window)
    globalvars.heroGroup.draw(globalvars.window)
    globalvars.attackGroup.draw(globalvars.window)
    pygame.display.update()
    clock.tick(FPS)
