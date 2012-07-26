# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

import sys
from constants import *
from globalvars import *
from menu import *
from sprites import *
from attacks import *
from vector import Vector
import pygame

class PC(NPC):
    """Sprite class for the Player Character.
    """
    def __init__(self, name, pos):
        NPC.__init__(self, name, "hero", pos)
        self.startloc = "milenariaW"
        self.speed = 2.5
        self.hp = 30
        self.hpmax = 30
        self.str = 3
        self.dex = 3
        self.weapon = "wrench"
        self.gun = "gun"
        self.sfxhurt = "malehurt.wav"
        self.sfxdead = "maledead.wav"
        self.potions = 3
        self.ammo = 20
        self.bombs = 50
        self.coins = 50
        self.keys = 1
        self.potiontimer = 0
        self.potiontimermax = POTIONTIMER
        self.bombtimermax = 360
        self.bombtimer = 0

    def tick(self):
        if self.potiontimer == self.potiontimermax:
            self.potiontimer = 0
        elif self.potiontimer > 0:
            self.potiontimer += 1
        if self.bombtimer == self.bombtimermax:
            self.bombtimer = 0
        elif self.bombtimer > 0:
            self.bombtimer += 1
        return NPC.tick(self)

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
            # drink a potion
            if self.potions >= 1 and self.potiontimer == 0 and self.hp < self.hpmax:
                sfxPlay("healed.wav")
                self.potions -= 1
                self.hp = self.hpmax
                self.potiontimer = 1
        if pressed[K_e]: # examined with 'E'
            aoe = self.space_ahead()
            for s in globalvars.solidGroup:
                if aoe.colliderect(s.rect) and s.name is not self.name:
                    choice = s.examine()
                    if choice and isinstance(s, Transition):
                        return s.direction
        if pressed[K_q]:
            # drop a bomb
            if self.bombs > 0 and self.bombtimer == 0:
                self.bombs -= 1
                globalvars.attackQ.add(Bomb(self))
                self.bombtimer = 1
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
        if mousebutton1 and self.weapon is not None:
            self.mattack()
        if mousebutton3 and self.gun is not None:
            self.rattack()
        # update movement rectangle
        vect = Vector(x, y)
        moveval = self.move(vect.normalize())
        # finalize
        self.animate()
        return moveval

    def get(self, item):
        """Analyize the item, add it to inventory, destroy it"""
        sfxPlay("pickup.wav")
        if item.name == "potion":
            self.potions += 1
        elif item.name == "powerbar":
            self.hpmax += 10
            self.hp = self.hpmax
        elif item.name == "ammo":
            self.ammo += 10
        elif item.name == "bomb":
            self.bombs += 1
        elif item.name == "coin":
            self.coins += 1
        elif item.name == "chest":
            self.coins += 10
        elif item.name == "key":
            self.keys += 1
        elif item.name == "wrench":
            menu.dialogue("You got a wrench!  Left-click to swing away!")
            self.weapon = "wrench"
        elif item.name == "gun":
            menu.dialogue("You got a gun!  Aim it with the cursor, fire with right-click!")
            menu.dialogue("You can only fire the gun if you have bullets.")
            self.gun = "gun"
        item.kill()

    def die(self):
        """Same as sprite.die, but nullify hero globalvar."""
        #global hero
        dialogue("You have died...")
        pygame.quit()
        sys.exit()
