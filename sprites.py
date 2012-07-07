from constants import *
from vector import Vector
from brain import *

"""needs class for animations
"""

class NPC(pygame.sprite.Sprite):
    """Sprite class for civilians
    """
    def __init__(self, name, spritename, images, pos): #pos = (x,y), images = dictionary 
        pygame.sprite.Sprite__init__(self)
        self.name = name
        self.images = images
        self.image = self.images[name+".frontStand.bmp"]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.destination = None #Tuple
        self.vector = None #Vector, normalized
        self.speed = 3
        self.brain = VillagerBrain()
        self.moving = False
        self.timer = ANIMTIMERFAST
        self.facing = "front"
        self.animation = ""

    """Returns the current facing of the sprite, based on movement vector
    """
    def getFacing():
        pass

    """Update the sprite to match current action
    """
    def animate():
        # update timer
        self.timer -= 1
        if self.timer < 0:
            self.timer = ANIMTIMERFAST
        # update animation
        

    def update(solidSprites):
        self.brain.think(solidSprites)

class CombatNPC(NPC):
    """Sprite class for NPCs that can fight
    """
    def __init__(self, name, pos):
        NPC.__init__(self, name, pos)
        self.images.update(imagesCombatNPC(self.name))
        self.attacking = False

    def update():
        pass

class PC(CombatNPC):
    """Sprite class for the Player Character
    """
    def __init__(self, name, pos):
        CombatNPC.__init__(self, name, pos)
        self.images.update(imagesPC(self.name))
        
        def update():
            pass
