# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from globalvars import *
from sprites import *
from attacks import *
from vector import Vector
import pygame

class PC(NPC):
    """Sprite class for the Player Character.
    """
    def __init__(self, name, pos):
        NPC.__init__(self, name, "hero", pos)
        self.speed = 2.5
        self.hp = 30
        self.str = 3
        self.dex = 3
        self.weapon = "wrench"
        self.gun = "gun"
        self.sfxhurt = "malehurt.wav"
        self.sfxdead = "maledead.wav"

    def update(self):
        """Update the hero sprite based on the user's iteraction.
        Returns direction if the user touches the edge of the map
          (i.e. "west" if user enters left edge of screen)
        Returns None if the user doesn't exit the screen.
        """
        #global solidGroup
        if not self.tick():
            return
        x = 0
        y = 0
        # perform actions for each key press
        pressed = pygame.key.get_pressed()
        if pressed[K_SPACE]:
            # for now, pressing SPACE animates a pose and stuns
            self.facing = "front"
            self.action = "Item"
            self.stuntimer = 1
            self.animate()
            return
        if pressed[K_e]: # examined with 'E'
            aoe = self.space_ahead()
            for s in globalvars.solidGroup:
                if aoe.colliderect(s.rect) and s.name is not self.name:
                    choice = s.examine()
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
            self.mattack()
        if mousebutton3:
            self.rattack()
        # update movement rectangle
        vect = Vector(x, y)
        moveval = self.move(vect.normalize())
        # finalize
        self.animate()
        return moveval

    def die(self):
        """Same as sprite.die, but nullify hero globalvar."""
        #global hero
        globalvars.hero = None
        NPC.die(self)
