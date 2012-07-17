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

pygame.init()

# Game constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont(None, 16)
FPS = 60
TILESIZE = 32
BOXSIZE = TILESIZE*3
CENTERTILEWIDTH = 16
BORDERTILEWIDTH = 8
DIAGONAL = 0.707106781187 # (1,1) vector normalized

# sprite constants
KNOCKBACK = 5
FLINCHTIMER = 10 # after getting hit, time period of invulnerability
WAITTIMER = 24 # used for attack waiting time
ATTACKTIMER = 8 # how long a weapon attack lasts, even number
GUNTIMER = 80
ANIMATETIMER = 20 # used for movement animations
MINTIME = 30 # time for moving or waiting (sort of like a 'turn')
MAXTIME = 120

# screen constants
CENTERWIDTH = TILESIZE*CENTERTILEWIDTH
CENTERHEIGHT = CENTERWIDTH
SCREENHEIGHT = CENTERWIDTH
BORDERWIDTH = TILESIZE*BORDERTILEWIDTH
CENTERXSTART = BORDERWIDTH
CENTERXEND = CENTERWIDTH + BORDERWIDTH
CENTERX = CENTERXEND - (CENTERWIDTH/2)
CENTERYSTART = 0
CENTERYEND = CENTERHEIGHT
CENTERY = CENTERYEND - (CENTERHEIGHT/2)
SCREENWIDTH = CENTERWIDTH+(BORDERWIDTH*2)
CENTERCENTER = (CENTERXSTART+(CENTERWIDTH/2), CENTERYSTART+(CENTERWIDTH/2))

# Functions

# Exceptions
class AIError(Exception):
    """AI Error when an action fails.
    """
    def __init__(self, msg=None):
        self.msg = msg

# Sound Effects

def sfxPlay(sfx):
    sfxfile = join("data", "sfx", sfx)
    pygame.mixer.Sound(sfxfile).play()

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

