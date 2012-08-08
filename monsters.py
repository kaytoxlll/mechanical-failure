# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from sprites import *
from brain import *
from random import seed, randint
import sys

class Rat(NPC):
    def __init__(self, pos=(0,0)):
        NPC.__init__(self, "Rat", "rat", pos)
        self.text = ["Squeak!"]
        self.speed = 3.5
        self.hp = 10
        self.str = 1
        self.dex = 0
        self.sfxhurt = "rathurt.wav"
        self.sfxdead = "ratdead.wav"
        self.brain = FighterBrain(self)
        
    def die(self):
        """Drop items, then die"""
        NPC.die(self)
        seed()
        dropchance = randint(1,100)
        if dropchance < 10:
            self.drop("potion")
        elif dropchance < 50:
            self.drop("coin")

class Thief(NPC):
    def __init__(self, pos=(0,0)):
        NPC.__init__(self, "Thief", "thief", pos)
        self.text = ["Gimme your money!"]
        self.speed = 2.5
        self.hp = 20
        self.str = 3
        self.dex = 0
        self.weapon = "sword"
        self.sfxhurt = "malehurt.wav"
        self.sfxdead = "maledead.wav"
        self.brain = FighterBrain(self)

    def die(self):
        NPC.die(self)
        seed()
        dropchance = randint(1,100)
        if dropchance < 10:
            self.drop("potion")
        elif dropchance < 30:
            self.drop("ammo")
        elif dropchance < 70:
            self.drop("coin")

class Boss(NPC):
    def __init__(self, pos=(0,0)):
        NPC.__init__(self, "Shadow", "boss", pos)
        self.text = ["Die, punk!"]
        self.speed = 3.5
        self.hp = 60
        self.str = 5
        self.dex = 0
        self.weapon = "sword"
        self.sfxhurt = "malehurt.wav"
        self.sfxdead = "maledead.wav"
        self.brain = FighterBrain(self)

    def die(self):
        menu.dialogue(globalvars.hero.name + ": Take that!")
        menu.dialogue(self.name + ": Argh...")
        menu.dialogue(self.name + " has died.")
        menu.dialogue(globalvars.hero.name + " has retrieved his wallet.")
        menu.dialogue("The end.")
        menu.dialogue("Thanks for playing!")
        pygame.quit()
        sys.exit()
    
