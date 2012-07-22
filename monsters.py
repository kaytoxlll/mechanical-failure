# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from sprites import *
from brain import *
from random import seed, randint

class Rat(NPC):
    def __init__(self, pos=(0,0)):
        NPC.__init__(self, "Rat", "rat", pos)
        self.text.append("Squeak!")
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
