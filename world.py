# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

import globalvars
from menu import *
import sprites
from monsters import *
from music import *
from os import getcwd, listdir
from os.path import join
import pygame
from random import seed, randint

"""This file defines variables used by the rest of the game:
currentmap = The current terrain/mobs on the screen, using:
  .obstacles
  .mobs

Scripts use the scriptdone boolean to know when to stop running the script.
script() returns True when it no longer needs to run.
"""

KEY = {".":'None',
       "!":'SavePoint("savepoint", "terrain", self.name)',
       "G":'Floor(self.floor2, "terrain")',
       "~":'Obstacle(self.water, "terrain", solid=False, animate=True)',
       "W":'Obstacle(self.wall, "terrain")',
       "X":'Obstacle("housezone", "terrain")', # 8x4
       "N":'Obstacle("window", "terrain")',
       "B":'Obstacle("barrel" + str(mod), "terrain", breakable=True)',
       "O":'Obstacle("box" + str(mod), "terrain", breakable=True)',
       "T":'Obstacle("toxicbarrel" + str(mod), "terrain")',
       "U":'Obstacle("bush" + str(mod), "terrain")',
       "H":'Obstacle(self.house + str(mod), "terrain")',
       "C":'Obstacle("counter", "terrain")',
       "S":'Obstacle("sludge", "terrain", solid=False, animate=True)',
       "M":'Obstacle("moat", "terrain", solid=False, animate=True)',
       "I":'Obstacle("lillypads", "terrain", solid=False, animate=True)',
       "D":'Moveable("doorwide", "terrain")',
       "d":'Moveable("doortall", "terrain")',
       "L":'Locked("lockwide", "terrain")',
       "l":'Locked("locktall", "terrain")',
       "E":'Explodeable(self.wall+"weak", "terrain")',
       "#":'Sign("sign", "terrain", self.sign)',
       "V":'Obstacle("vendingmachine", "terrain")',
       "<":'Transition("ladderdown", "terrain", "down")',
       ">":'Transition("ladderup", "terrain", "up")',
       "Z":'Transition("zone", "terrain", "north")', 
       "P":'ShopItem("potion", 20)',
       "A":'ShopItem("ammo", 10)',
       "Q":'ShopItem("bomb", 50)',
       "p":'Item("potion")',
       "b":'Item("powerbar")',
       "a":'Item("ammo")',
       "o":'Item("bomb")',
       "c":'Item("coin")',
       "h":'Item("chest")',
       "k":'Item("key")',
       "w":'Item("wrench")',
       "g":'Item("gun")',
       "r":'Rat()',
       "t":'Thief()',
       "n":'NPC(self.npcname, self.npcref, (0,0), self.npclines)'}
       
class Map():
    """Contains all the info for a reigon of the screen."""
    def __init__(self, filename):
        self.script = None
        self.script2 = None
        self.scriptdone = False
        self.script2done = False
        execfile(join("data", "maps", filename))
        self.name = filename[:-3]
        # set area type variables
        if self.type == "slum":
            self.song = "slums.mp3"
            self.floor = "stone"
            self.floor2 = "grass"
            self.wall = "brick"
            self.wall2 = "beams"
            self.water = "water"
            self.house = "house"
        elif self.type == "house":
            self.song = "town.mp3"
            self.floor = "boards"
            self.floor2 = "slab"
            self.wall = "beams"
            self.water = "water"
        elif self.type == "sewer":
            self.song = "sewer.mp3"
            self.floor = "slime"
            self.floor2 = "stone"
            self.wall = "slab"
            self.water = "sewage"
        elif self.type == "rich":
            self.song = "garden.mp3"
            self.floor = "pastelstone"
            self.floor2 = "grass"
            self.wall = "pastelbrick"
            self.wall2 = "beams"
            self.water = "water"
            self.house = "pastelhouse"
        elif self.type == "garden":
            self.song = "garden.mp3"
            self.floor = "grass"
            self.floor2 = "stone"
            self.wall = "pastelbrick"
            self.water = "water"
            self.house = "pastelhouse"
        # set script variables
        self.scripttext = []
        if self.script is not None:
            if self.script[0] == "doors":
                self.script = self.doorscript
            else:
                self.scripttext = self.script
                self.script = self.dialoguescript
        else:
            self.scriptdone = True
        if self.script2 is not None:
            if self.script2[0] == "doors":
                self.script2 = self.doorscript
            else:
                self.scripttext = self.script2
                self.script2 = self.dialoguescript
        else:
            self.script2done = True
        self.floor = globalvars.images["terrain" + self.floor]
        self.obstacles = pygame.sprite.Group()
        self.moveableGroup = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.backgroundGroup = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        self.surfaceGroup = pygame.sprite.Group()
        x = CENTERXSTART
        y = CENTERYSTART
        for line in self.grid:
            for char in line:
                mod = randint(1,2)
                sprite = eval(KEY[char])
                if isinstance(sprite, sprites.Floor):
                    sprite.rect.topleft = (x,y)
                    self.backgroundGroup.add(sprite)
                elif isinstance(sprite, sprites.ShopItem):
                    sprite.rect.center = (x+TILESIZE/2, y+TILESIZE/2)
                    self.obstacles.add(sprite)
                    self.surfaceGroup.add(sprite)
                elif isinstance(sprite, sprites.Item):
                    sprite.rect.center = (x+TILESIZE/2 ,y+TILESIZE/2)
                    self.itemGroup.add(sprite)
                elif sprite is not None and sprite.name == "vendingmachine":
                    sprite.rect.topleft = (x, y-TILESIZE)
                    self.obstacles.add(sprite)
                elif type(sprite) == Moveable:
                    sprite.rect.topleft = (x,y)
                    self.moveableGroup.add(sprite)
                elif isinstance(sprite, NPC):
                    sprite.rect.topleft = (x,y)
                    self.mobs.add(sprite)
                elif isinstance(sprite, Transition):
                    sprite.rect.topleft = (x,y)
                    self.obstacles.add(sprite)
                    self.backgroundGroup.add(sprite)
                elif isinstance(sprite, Obstacle):
                    sprite.rect.topleft = (x,y)
                    self.obstacles.add(sprite)
                elif char is not ".":
                    print "Error: unknown sprite type:", char
                x += TILESIZE
            y += TILESIZE
            x = CENTERXSTART

    """Map scripts all return True when the script no longer needs
    to execute, and return False if the script still needs to run each turn.
    """
    def dialoguescript(self):
        for line in self.scripttext:
            menu.dialogue(line)
        return True

    def doorscript(self):
        """when all the enemies are killed, open the doors"""
        if len(self.mobs) == 0:
            for s in self.moveableGroup:
                s.kill()
            return True
        else:
            return False

class World():
    """Contains all the maps, notable the current map."""
    def __init__(self):
        seed()
        self.maps = {}
        path = join(getcwd(), "data", "maps")
        maplist = listdir(path)
        for m in maplist:
            self.maps[m[:-3]] = Map(m)
        self.currentmap = self.maps[globalvars.hero.startloc]
        self.music = MusicPlayer(self.currentmap.song)
        globalvars.solidGroup.add(self.currentmap.obstacles)
        globalvars.solidGroup.add(self.currentmap.moveableGroup)
        globalvars.solidGroup.add(self.currentmap.mobs)
        globalvars.itemGroup.add(self.currentmap.itemGroup)
        self.draw(globalvars.window)
        pygame.display.update()
        # hero initializes to centercenter

    def load(self, herofromdirection):
        """Load the contents for the next map area.
        Positions the hero based on his direction ("north", etc).
        """
        globalvars.attackGroup.empty()
        if herofromdirection == "north": # starts south
            self.currentmap = self.maps[self.currentmap.north]
            globalvars.hero.rect.topleft = (CENTERX-TILESIZE/2, CENTERYEND-TILESIZE)
        elif herofromdirection == "south": # starts north
            self.currentmap = self.maps[self.currentmap.south]
            zone = False
            for s in self.currentmap.obstacles:
                if s.name == "zone":
                    globalvars.hero.rect.topleft = s.rect.move(0, TILESIZE).topleft
                    zone = True
                    break
            if not zone:
                globalvars.hero.rect.topleft = (CENTERX-TILESIZE/2, CENTERYSTART)
        elif herofromdirection == "east": # starts west
            self.currentmap = self.maps[self.currentmap.east]
            globalvars.hero.rect.topleft = (CENTERXSTART, CENTERY-TILESIZE/2)
        elif herofromdirection == "west": # starts east
            self.currentmap = self.maps[self.currentmap.west]
            globalvars.hero.rect.topleft = (CENTERXEND-TILESIZE, CENTERY-TILESIZE/2)
        elif herofromdirection == "down":
            self.currentmap = self.maps[self.currentmap.down]
            globalvars.hero.rect.center = CENTERCENTER
            for s in self.currentmap.obstacles:
                if isinstance(s, Transition):
                    globalvars.hero.rect = s.rect.move(0, TILESIZE)
        elif herofromdirection == "up":
            self.currentmap = self.maps[self.currentmap.up]
            globalvars.hero.rect.center = CENTERCENTER
            for s in self.currentmap.obstacles:
                if isinstance(s, Transition):
                    globalvars.hero.rect = s.rect.move(0, TILESIZE)
        else:
            globalvars.hero.rect.center = CENTERCENTER
        # remove any obstacles the hero intersects with
        pygame.sprite.spritecollide(globalvars.hero, self.currentmap.obstacles, True)
        pygame.sprite.spritecollide(globalvars.hero, self.currentmap.moveableGroup, True)
        #set up music and groups
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
        self.currentmap.obstacles.update()
        self.currentmap.mobs.update()
        if not self.currentmap.scriptdone:
            self.currentmap.scriptdone = self.currentmap.script()
        if not self.currentmap.script2done:
            self.currentmap.script2done = self.currentmap.script2()

    def draw(self, window):
        """Draw the floor, obstacles, background (blood), attacks, and mobs"""
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
        self.currentmap.surfaceGroup.draw(globalvars.window)
        self.currentmap.moveableGroup.draw(globalvars.window)
        self.currentmap.itemGroup.draw(globalvars.window)
        globalvars.attackGroup.draw(globalvars.window)
        self.currentmap.mobs.draw(globalvars.window)
