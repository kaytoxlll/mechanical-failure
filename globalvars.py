# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from images import *
from pc import PC

# global images
images = loadAllImages()

# global sprite groups
solidGroup = pygame.sprite.Group()
solidQ = pygame.sprite.Group()
backgroundQ = pygame.sprite.Group()
attackQ = pygame.sprite.Group()
newitemQ = pygame.sprite.Group()
hero = PC("Cole", CENTERCENTER)
