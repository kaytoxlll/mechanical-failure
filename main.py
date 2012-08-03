# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

import sys
from os import getcwd, listdir
from os.path import join
from constants import *
from globalvars import *
from world import *
import sprites
import pc
from monsters import *
import menu
import pygame

# initialization
pygame.mixer.init()
pygame.display.set_caption("Mechanical Failure")
pygame.display.set_icon(globalvars.images["misc" + "logo"])

while True:
    if globalvars.newgame:
        # load save game
        globalvars.hero = pc.PC("Cole", CENTERCENTER)
        globalvars.heroGroup.empty()
        globalvars.heroGroup.add(globalvars.hero)
        globalvars.solidGroup.empty()
        globalvars.solidGroup.add(globalvars.hero)
        globalvars.attackGroup.empty()
        globalvars.itemGroup.empty()
        path = join(getcwd(), "savedata")
        savelist = listdir(path)
        if len(savelist) > 1:
            if menu.dialogue("Do you want to load the saved game?"):
                menu.load("save1.py")
            else:
                menu.get_name()
        else:
            menu.get_name()
        # set up groups
        world = World()
        globalvars.newgame = False
    
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
    world.currentmap.surfaceGroup.add(globalvars.backgroundQ)
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
    pygame.display.update()
    globalvars.clock.tick(FPS)
