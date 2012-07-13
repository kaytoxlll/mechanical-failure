# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from os.path import join
import pygame
from pygame.locals import *

"""variables set up the screen like this:
-------------
| |       | |
| |       | |
-------------
where the side rectangles are for HUD

todo: make music its own library, along with SFX
"""

# Game variables
FPS = 60
WAITTIMER = 30 # used for attack waiting time
ATTACKTIMER = 10 # how long a weapon attack lasts
ANIMATETIMER = 20 # used for movement animations
TILESIZE = 32
CENTERTILEWIDTH = 16
BORDERTILEWIDTH = 8
DIAGONAL = 0.707106781187 # (1,1) vector normalized

# Derived variables
CENTERWIDTH = TILESIZE*CENTERTILEWIDTH
CENTERHEIGHT = CENTERWIDTH
SCREENHEIGHT = CENTERWIDTH
BORDERWIDTH = TILESIZE*BORDERTILEWIDTH
CENTERXSTART = BORDERWIDTH
CENTERXEND = CENTERWIDTH + BORDERWIDTH
CENTERYSTART = 0
CENTERYEND = CENTERHEIGHT
SCREENWIDTH = CENTERWIDTH+(BORDERWIDTH*2)
CENTERCENTER = (CENTERXSTART+(CENTERWIDTH/2), CENTERYSTART+(CENTERWIDTH/2))

# Functions

# Exceptions
class AIError(Exception):
    """AI Error when an action fails.
    """
    def __init__(self, msg=None):
        self.msg = msg

# Music
def songPlay(song):
    songfile = join("data", "music", song)
    pygame.mixer.music.load(songfile)
    pygame.mixer.music.play(-1, 0.0)

def songStop():
    pygame.mixer.music.stop()

def songPause():
    pygame.mixer.music.pause()

def songUnpause():
    pygame.mixer.music.unpause()

def songFadeout():
    pygame.mixer.music.fadeout(1000)

