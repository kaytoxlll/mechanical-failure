# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

import globalvars
from sprites import *
from monsters import *
from music import *
from os import getcwd, listdir
from os.path import join
import pygame

"""This file defines variables used by the rest of the game:
currentmap = The current terrain/mobs on the screen, using:
  .obstacles
  .mobs

Scripts use the scriptdone boolean to know when to stop running the script.
script() returns True when it no longer needs to run.
"""

KEY = {".":'None', 
       "w":'Obstacle("wall", "terrain")', 
       "b":'Obstacle("barrel", "terrain")', 
       "h":'Obstacle("house1", "terrain")', 
       "r":'Rat()',
       "n":'NPC(self.npcname, self.npcref, (0,0), self.npclines)',
       "p":'Item("potion")',
       "a":'Item("ammo")',
       "c":'Item("coin")',
       "P":'ShopItem("potion", 20)',
       "A":'ShopItem("ammo", 10)',
       "D":'Moveable("doorwide", "terrain")',
       "d":'Moveable("doortall", "terrain")'}

class Map():
    """Contains all the info for a reigon of the screen."""
    def __init__(self, file):
        execfile(join("data", "maps", file))
        #self.name = name
        #self.song = song
        #self.script = script
        self.floor = globalvars.images["terrain" + self.floor]
        #self.east = east
        #self.west = west
        #self.north = north
        #self.south = south
        self.scriptdone = False
        self.obstacles = pygame.sprite.Group()
        self.moveableGroup = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.backgroundGroup = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        x = CENTERXSTART
        y = CENTERYSTART
        for line in self.grid:
            for char in line:
                sprite = eval(KEY[char])
                sprite.rect.topleft = (x,y)
                if type(sprite) == Item:
                    self.itemGroup.add(sprite)
                elif type(sprite) == Moveable:
                    self.moveableGroup.add(Sprite)
                elif isinstance(sprite, Obstacle):
                    self.obstacles.add(sprite)
                elif isinstance(sprite, NPC):
                    self.mobs.add(sprite)
                x += TILESIZE
            y += TILESIZE
            x = CENTERXSTART

class World():
    """Contains all the maps, notable the current map."""
    def __init__(self):
        self.maps = {}
        path = join(getcwd(), "data", "maps")
        maplist = listdir(path)
        for m in maplist:
            self.maps[m[:-3]] = Map(m)
        self.currentmap = self.maps["start"]
        self.music = MusicPlayer(self.currentmap.song)
        globalvars.solidGroup.add(self.currentmap.obstacles)
        globalvars.solidGroup.add(self.currentmap.moveableGroup)
        globalvars.solidGroup.add(self.currentmap.mobs)
        globalvars.itemGroup.add(self.currentmap.itemGroup)
        # hero initializes to centercenter

    def load(self, herofromdirection):
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
        self.music.play(self.currentmap.song)
        globalvars.solidGroup.empty()
        globalvars.solidGroup.add(self.currentmap.obstacles)
        globalvars.solidGroup.add(self.currentmap.moveableGroup)
        globalvars.solidGroup.add(globalvars.hero)
        globalvars.solidGroup.add(self.currentmap.mobs)
        globalvars.itemGroup.empty()
        globalvars.itemGroup.add(self.currentmap.itemGroup)
        # draw screen before script
        self.draw(globalvars.window)
        globalvars.heroGroup.draw(globalvars.window)
        pygame.display.update()

    def update(self):
        """Update all the mob sprites, run script"""
        self.currentmap.mobs.update()
        if not self.currentmap.scriptdone:
            self.currentmap.scriptdone = self.currentmap.script()

    def draw(self, window):
        """Draw the floor, obstacles, background (blood), and mobs"""
        # draw the ground
        x = CENTERXSTART
        y = CENTERYSTART
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
        self.currentmap.obstacles.draw(globalvars.window)
        self.currentmap.backgroundGroup.draw(globalvars.window)
        self.currentmap.itemGroup.draw(globalvars.window)
        self.currentmap.mobs.draw(globalvars.window)
