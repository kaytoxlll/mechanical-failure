# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from sprites import *
from brain import *

class Rat(NPC):
    def __init__(self, images, pos):
        NPC.__init__(self, "Rat", "rat", images, pos)
        self.speed = 3.5
        # self.brain = ThiefBrain(self)
        
