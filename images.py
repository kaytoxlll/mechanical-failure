# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from os import getcwd, listdir
from os.path import join

def loadAllImages():
    """ Returns a dictionary of all the sprites used in the game.
        Dictionary maps a string key to the Surface image.
        usage: data/images/hero/frontStand.bmp
        will be images["herofrontStand"]
    """
    images = {}
    path = join(getcwd(), "data", "images")
    directories = listdir(path)
    for directory in directories:
        subpath = join(path, directory)
        subdirectories = listdir(subpath)
        for imagefile in subdirectories:
            image = pygame.image.load(join(subpath, imagefile))
            images[directory+imagefile[0:len(imagefile)-4]] = image
    return images

# test
#print loadAllImages()
