# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from sprites import *
from attacks import *
from vector import Vector
import pygame

class PC(NPC):
    """Sprite class for the Player Character.
    """
    def __init__(self, name, images, pos):
        NPC.__init__(self, name, "hero", images, pos)
        self.weapon = "wrench"

    def update(self, solidSprites):
        """Update the hero sprite based on the user's iteraction.
        Returns a group of new sprites, maybe empty.
        """
        newsprites = pygame.sprite.Group()
        if self.tick() is False:
            return newsprites
        x = 0
        y = 0
        # perform actions for each key press
        pressed = pygame.key.get_pressed()
        if pressed[K_SPACE]:
            # for now, pressing SPACE animates a pose and stuns
            self.facing = "front"
            action = "Item"
            self.stuntimer = 1
            self.animate(action)
            return newsprites
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
        # perform actions for mouse buttons pressed
        (mousebutton1, mousebutton2, mousebutton3) = pygame.mouse.get_pressed()
        if mousebutton1:
            newsprites.add(self.mattack())
        # update movement rectangle
        vect = Vector(x, y)
        moveval = self.move(vect, solidSprites)
        # finalize
        self.animate()
        return newsprites
