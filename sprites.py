from constants import *
from vector import Vector
from brain import *
from pygame

"""needs combatnpc.update()
"""

class Obstacle():
    """Base sprite class for map objects (i.e. barrels, etc)
    """
    def __init__(self, name, reference, images, pos, solid):
        pygame.sprite.Sprite.__init__(self)
        self.ref = reference # i.e. terrain (directory)
        self.name = name # i.e. barrel (file name)
        self.image = images[self.ref + self.name]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos # i.e. (0,0) or (128, 64)
        self.solid = solid # boolean

    def update(solidSprites):
        pass

class NPC(pygame.sprite.Sprite):
    """Base sprite class for characters.
       Sprite class for civilians
    """
    def __init__(self, name, reference, images, pos): #pos = (x,y), images = dictionary 
        pygame.sprite.Sprite__init__(self)
        self.name = name # i.e. Bob
        self.ref = reference # i.e. VillagerMan
        self.images = images
        self.facing = "front"
        self.action = "Stand" # Stand, Walk1, Walk2
        self.image = self.images[self.ref + self.face + self.action]
        self.walk1 = self.images[self.ref + self.face + "Walk1"]
        self.walk2 = self.images[self.ref + self.face + "Walk2"]
        self.nextimage = None
        self.rect = self.image.get_rect()
        self.rect.topleft = pos # i.e. (0,0) or (128, 64)
        self.destination = None #Tuple
        self.vector = None #Vector, normalized
        self.speed = 3
        self.brain = VillagerBrain()
        self.moving = False
        self.timermax = ANIMATETIMER
        self.timer = 0 # increment to timermax, then reset to 0

    """Update the sprite to match current action
    """
    def animate(action=None):
        """Determines the current image to use and assigns it to self.image
           action = "Stand", "Walk1", etc
        """
        if action is not None:
            # update image and reset timer
            self.action = action
            self.image = self.images[self.ref + self.face + self.action]
            self.timer = 0
            return
        if self.timer = self.timermax and moving == True:
            # update the walking sprite
            if self.image == self.walk1:
                self.image = self.walk2
            else: self.image = self.walk1
        # update timer
        if self.timer == self.timermax:
            self.timer = 0
        else:
            self.timer += 1

    def update(solidSprites):
        self.brain.think(solidSprites)

class CombatNPC(NPC):
    """Sprite class for NPCs that can fight
    """
    def __init__(self, name, reference, images, pos, hp, armor):
        NPC.__init__(self, name, reference, images, pos)
        self.attacking = False
        self.hp = hp
        self.armor = armor
        self.attacktimermax = ATTACKTIMER
        self.attacktimer = 0 

    def update(solidSprites):
        pass

class PC(CombatNPC):
    """Sprite class for the Player Character
    """
    def __init__(self, name, images, pos, hp, armor):
        CombatNPC.__init__(self, name, "hero", images, pos, hp, armor)
        self.stuntimermax = ATTACKTIMER
        self.stuntimer = 0 # increment to max then reset to 0

    def update(solidSprites):
        """Update the hero sprite based on the user's iteraction
        """
        # check stunned timer first
        if self.stunnedtimer > 0:
            if self.stuntimer >= self.stuntimermax
                self.stuntimer = 0
                return
            self.stuntimer += 1
            return
        # reset variables
        self.moving = False
        x = 0
        y = 0
        # perform actions for each key press
        pressed = pygame.key.get_pressed()
        if pressed[K_SPACE]:
            # for now, pressing SPACE animates a pose and stuns
            self.animate("Item")
            self.stuntimer = 1
            return
        if pressed[K_w]: # up
            y = -1
            self.facing = "back"
            self.moving = True
        elif pressed[K_s]: # down
            y = 1
            self.facing = "front"
            self.moving = True
        if pressed[K_a]: # left
            x = -1
            self.facing = "left"
            self.moving = True
        elif pressed[K_d]: # right
            x = 1
            self.facing = "right"
            self.moving = True
        # update movement rectangle
        vect = Vector(x, y).normalize()
        dist = vect * self.speed
        newrect = self.rect.move(dist)
        if newrect.bottom > CENTERYEND:
            newrect = self.rect # reset the rect if out of bounds
        elif newrect.top < CENTERYSTART:
            newrect = self.rect
        if newrect.left < CENTERXSTART:
            newrect = self.rect
        elif newrect.right > CENTERXEND:
            newrect = self.rect
        self.rect = newrect
        self.animate()
