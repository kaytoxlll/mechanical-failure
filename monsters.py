# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from sprites import *
from brain import *

class Rat(NPC):
    def __init__(self, images, pos):
        NPC.__init__(self, "Rat", "rat", pos)
        self.speed = 3.5
        self.hp = 10
        self.str = 1
        self.dex = 0
        self.sfxhurt = "rathurt.wav"
        self.sfxdead = "ratdead.wav"
        # self.brain = ThiefBrain(self)
        
