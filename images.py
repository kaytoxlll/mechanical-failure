from constants import *

"""
todo: this file should maintain a dictionary of each file the game uses.
by default it will load all images when the game starts.
the dictionary key for each file (Surface) will be the file name minus
the extension (i.e. heroFront -> heroFront.bmp
each file needs a unique name.

functions:
primary use will be querying the dictionary (not a function)
possibly init functions for different dictionaries (for each area)
and delete funtions (or just del) to free memory

possible problems:
only one copy of each image means the origin cannot be modiied, such
as by rotating an arrow image.
if this causes loading performance problems it can later be made to 
load images for certain areas, plus images common to all areas, such 
as the hero.
"""

"""Each function returns a dictionary mapping image names to Surface"""

def loadImage(imagename): #deprecate
    imagefile = join("data", "images", imagename)
    return pygame.image.load(imagefile).convert_alpha()

def loadSpriteImage(spritename, imagename):
    imagefile = join("data", "images", spritename, imagename)
    return pygame.image.load(imagefile).convert_alpha()

def imagesNPC(name): #dict(string:Surface)
    return {
        "frontStand":loadSpriteImage(name, "frontStand.bmp"),
        "frontWalk1":loadSpriteImage(name, "frontWalk1.bmp"),
        "frontWalk2":loadSpriteImage(name, "frontWalk2.bmp"),
        "leftStand":loadSpriteImage(name, "leftStand.bmp"),
        "leftWalk1":loadSpriteImage(name, "leftWalk1.bmp"),
        "leftWalk2":loadSpriteImage(name, "leftWalk2.bmp"),
        "rightStand":loadSpriteImage(name, "rightStand.bmp"),
        "rightWalk1":loadSpriteImage(name, "rightWalk1.bmp"),
        "rightWalk2":loadSpriteImage(name, "rightWalk2.bmp"),
        "backStand":loadSpriteImage(name, "backStand.bmp"),
        "backWalk1":loadSpriteImage(name, "backWalk1.bmp"),
        "backWalk2":loadSpriteImage(name, "backWalk2.bmp")
        }

def imagesCombatNPC(name):
    return {
        "frontAttack":loadSpriteImage(name, "frontAttack.bmp"), 
        "leftAttack":loadSpriteImage(name, "leftAttack.bmp"), 
        "rightAttack":loadSpriteImage(name, "rightAttack.bmp"), 
        "backAttack":loadSpriteImage(name, "backAttack.bmp")
        }

def imagesPC(name):
    return {"gotItem":loadSpriteImage(name, "gotItem.bmp")}
