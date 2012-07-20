# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from images import *
from pc import PC

# global pygame thingies
window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

# global images
images = loadAllImages()

# global PC
hero = PC("Cole", CENTERCENTER)

# global sprite groups
heroGroup = pygame.sprite.Group(hero)
backgroundGroup = pygame.sprite.Group()
solidGroup = pygame.sprite.Group(heroGroup)
attackGroup = pygame.sprite.Group()
solidQ = pygame.sprite.Group()
backgroundQ = pygame.sprite.Group()
attackQ = pygame.sprite.Group()
newitemQ = pygame.sprite.Group()
