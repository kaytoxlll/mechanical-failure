from images import *
from math import fabs
from vector import Vector

"""
needs vector class for movement
need to be more object oriented:
move destination, vector, etc to brain
"""

class NPC(pygame.sprite.Sprite):
    """Sprite class for civilians"""
    def __init__(self, name, pos): #pos = (x,y)
        pygame.sprite.Sprite__init__(self)
        self.name = name
        self.images = imagesNPC(self.name)
        self.image = images["frontStand"]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.destination = None #Tuple
        self.vector = None #Vector2, normalized
        self.speed = 3
        self.brain = StateMachine()
        self.brain.addState(Wandering(self))
        self.moving = False
        self.animTimer = ANIMTIMERFAST
        self.direction = "front"

    """Returns the current facing of the sprite, based on movement vector"""
    def getFacing():
        if vector is None:
            return "front"
        xabs = fabs(self.vector.x)
        yabs = fabs(self.vector.y)
        if xabs > yabs:
            if self.vector.x > 0:
                
        elif yabs < 

    """Move toward the destinaton tuple"""
    def move(): #needs collision detection
        if self.vector is not None:
            distance = self.vector * self.speed
            self.rect.move_ip(distance)

    """Update the sprite to match current action"""
    def animate():
        if self.moving:
            self.animTimer -= 1
            if self.animTimer < 0:
                self.animTimer = ANIMTIMERFAST
            if self.animTimer == 0:
                if self.image == self.images["

    def update(spritesOnScreen):
        self.brain.think(spritesOnScreen)

class CombatNPC(NPC):
    """Sprite class for NPCs that can fight"""
    def __init__(self, name, pos):
        NPC.__init__(self, name, pos)
        self.images.update(imagesCombatNPC(self.name))
        self.attacking = False

    def update():
        pass

class PC(CombatNPC):
    """Sprite class for the Player Character"""
    def __init__(self, name, pos):
        CombatNPC.__init__(self, name, pos)
        self.images.update(imagesPC(self.name))
        
        def update():
            pass
