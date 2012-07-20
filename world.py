# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

import globalvars
from os import getcwd, listdir
from os.path import join
import pygame

"""This file defines variables used by the rest of the game:
currentmap = The current terrain/mobs on the screen, using:
  .obstacles
  .mobs
"""

KEY = {".":'None', 
       "w":'Obstacle("wall", "terrain")', 
       "b":'Obstacle("barrel", "terrain")', 
       "h":'Obstacle("house1", "terrain")', 
       "r":'Rat()', 
       "1":'one'}

class Map():
    """Contains all the info for a reigon of the screen."""
    def __init__(self, file):
        execfile(file)
        self.name = name
        floorimage = globalvars.images["terrain" + "floor" + floor]
        self.floor = pygame.Surface
        self.east = east
        self.west = west
        self.north = north
        self.south = south
        self.obstacles = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        x = 0
        y = 0
        for line in grid:
            for char in line:
                sprite = eval(KEY[char])
                if isinstance(sprite, Obstacle):
                    sprite.rect.topleft = (x,y)
                    self.obstacles.add(sprite)
                elif isinstance(sprite, NPC):
                    sprite.rect.topleft = (x,y)
                    self.mobs.add(sprite)
                x += TILESIZE
            y += TILESIZE

class World():
    """Contains all the maps, notable the current map."""
    def __init__(self):
        self.maps = {}
        path = join(getcwd(), "data", "maps")
        maplist = listdir(path)
        for m in maplist:
            self.maps[m[:-3]] = Map(m)
        self.currentmap = maps["start"]
        globalvars.solidGroup.add(currentmap.obstacles)
        globalvars.solidGroup.add(currentmap.mobs)
        # hero initializes to centercenter

    def load(herofromdirection):
        """Load the contents for the next map area.
        Positions the hero based on his direction ("north", etc).
        """
        if herofromdirection == "north": # starts south
            self.currentmap = self.maps[self.currentmap.north]
            globalvars.hero.rect.topleft = (CENTERX-TILESIZE/2, CENTERYEND-TILESIZE)
        elif herofromdirection == "south": # starts north
            self.currentmap = self.maps[self.currentmap.south]
            globalvars.hero.rect.topleft = (CENTERX-TILESIZE/2, CENTERYSTART)
        elif herofromdirection == "east": # starts west
            self.currentmap = self.maps[self.currentmap.east]
            globalvars.hero.rect.topleft = (CENTERXSTART, CENTERY-TILESIZE/2)
        elif herofromdirection == "west": # starts east
            self.currentmap = self.maps[self.currentmap.west]
            globalvars.hero.rect.topleft = (CENTERXEND-TILESIZE, CENTERY-TILESIZE/2)
        else:
            globalvars.hero.rect.center = CENTERCENTER
        globalvars.solidGroup.empty()
        globalvars.solidGroup.add(currentmap.obstacles)
        globalvars.solidGroup.add(currentmap.mobs)

    def update(self):
        """Update all the mob sprites"""
        self.currentmap.mobs.update()

    def draw(window):
        """Draw the floor, obstacles, and mobs"""
        # draw the ground
        x= CENTERXSTART
        y= CENTERYSTART
        image = self.currentmap.floor
        xinc = image.get_width()
        yinc = image.get_height()
        while y < CENTERYEND:
            while x < CENTERXEND:
                window.blit(image, (x,y))
                x += xinc
            y += yinc
            x=CENTERXSTART
        # draw the sprites.
        self.currentmap.obstacles.draw(window)
        self.currentmap.mobs.draw(window)
