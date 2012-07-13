# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from vector import Vector
from brain import *
import pygame
import random

"""To do:
update hit() methods
update or remove attack() methods
"""

class Obstacle(pygame.sprite.Sprite):
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

    def update(self):
        """Do what you do, which is probably nothing.
        """
        pass

    def hit(self, damage):
        """Just got hit by an attack.
        """
        pass

class NPC(pygame.sprite.Sprite):
    """Base sprite class for characters.
    Sprite class for civilians
    """
    def __init__(self, name, reference, images, pos): #pos = (x,y), images = dictionary 
        pygame.sprite.Sprite.__init__(self)
        self.name = name # i.e. Bob
        self.ref = reference # i.e. VillagerMan
        self.images = images
        self.facing = "front"
        self.action = "Stand" # Stand, Walk1, Walk2
        self.image = self.images[self.ref + self.facing + self.action]
        self.anim = True # boolean, used to swap movement animations
        self.rect = self.image.get_rect()
        self.rect.topleft = pos # i.e. (0,0) or (128, 64)
        self.attack = None # i.e. 
        self.shots = [] # ranged attacks in motion
        self.speed = 2.5
        self.hp = 100
        self.str = 0 # Strength, melee damage
        self.dex = 0 # Dexterity, ranged damage
                     # if str (dex) == 0 then cannot attack
        self.item = None # item dropped if killed
        self.dropchance = 50 # percent chance that items will drop
        self.brain = VillagerBrain(self)
        self.moving = False
        self.attacked = False # reset each frame
        self.animtimermax = ANIMATETIMER
        self.animtimer = 0 # increment to timermax, then reset to 0
        self.stuntimermax = ANIMATETIMER
        self.stuntimer = 0 # increment to stuntimermax then reset to 0

    def space_ahead(self):
        """Returns a rectangle space directly in front of the npc.
        """
        x = 0
        y = 0
        if self.facing == "front":
            x = TILESIZE
        elif self.facing == "back":
            x = -TILESIZE
        elif self.facing == "left":
            y = -TILESIZE
        elif self.facing == "right":
            y = TILESIZE
        return self.rect.move(x,y)

    def hit(self, damage):
        """Just got hit by an attack.
        """
        self.attacked = True
        pass

    def attack(self, target):
        """Not sure if I want to keep this method yet...
        """
        target.hit()
        pass

    def move(self, vector, solidSprites):
        """Attempt to move the sprite based on the vector.
        Modifies the moving flag accordingly.
        If there is a collision with the solid sprites or the map edge,
        return "success", else return the name of the collided-with object.
        This could also be an edge, i.e. "west" for the left edge of the screen.
        """
        if vector is None or (vector.x==0.0 and vector.y==0.0):
            # no distance to move
            self.moving = False
            return "success" 
        distance = vector.normalize() * self.speed
        newrect = self.rect.move(*distance.as_tuple())
        if newrect.bottom > CENTERYEND:
            self.moving = False
            return "south"
        elif newrect.top < CENTERYSTART:
            self.moving = False
            return "north"
        elif newrect.left < CENTERXSTART:
            self.moving = False
            return "west"
        elif newrect.right > CENTERXEND:
            self.moving = False
            return "east"
        for s in solidSprites:
            if newrect.colliderect(s.rect) and self.name is not s.name:
                self.moving = False
                return s.name
        self.rect = newrect
        self.moving = True
        return "success"

    def animate(self, action=None):
        """Determines the current image to use and assigns it to self.image
        action = "Stand", "Walk1", etc
        """
        if action is not None:
            # update image and reset timer
            self.action = action
            self.image = self.images[self.ref + self.action]
            self.animtimer = ANIMATETIMER - ATTACKTIMER
            return
        if self.animtimer == self.animtimermax and self.moving == True:
            # full timer (1/1), update walk animation
            if self.anim:
                self.image = self.images[self.ref + self.facing + "Walk1"]
            else:
                self.image = self.images[self.ref + self.facing + "Walk2"]
            self.anim = not self.anim
        elif self.animtimer == self.animtimermax / 2 and self.moving:
            # half timer (0.5/1), update stand animation
            self.image = self.images[self.ref + self.facing + "Stand"]
        elif self.moving == False:
            self.image = self.images[self.ref + self.facing + "Stand"]
        # update timer
        if self.animtimer == self.animtimermax:
            self.animtimer = 0
        else:
            self.animtimer += 1

    def update(self, solidSprites):
        """Process actions for the sprite each frame,
        Includes AI directives and animations.
        """
        self.brain.think(solidSprites)
        self.animate()
        self.attacked = False

    def die(self):
        """The sprite had died.
        Returns dropped item, or None if no item is dropped
        """
        self.kill()
        pass

class PC(NPC):
    """Sprite class for the Player Character
    """
    def __init__(self, name, images, pos):
        NPC.__init__(self, name, "hero", images, pos)

    def update(self, solidSprites):
        """Update the hero sprite based on the user's iteraction
        """
        # check stunned timer first
        if self.stuntimer > 0:
            if self.stuntimer >= self.stuntimermax:
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
        if pressed[K_a]: # left
            x = -1
            self.facing = "left"
            self.moving = True
        elif pressed[K_d]: # right
            x = 1
            self.facing = "right"
            self.moving = True
        if pressed[K_w]: # up
            y = -1
            self.facing = "back"
            self.moving = True
        elif pressed[K_s]: # down
            y = 1
            self.facing = "front"
            self.moving = True
        # update movement rectangle
        vect = Vector(x, y)
        moveval = self.move(vect, solidSprites)
        # finalize
        self.animate()
