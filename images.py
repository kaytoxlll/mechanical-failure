from constants import *

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
