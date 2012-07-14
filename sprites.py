# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from vector import Vector
from brain import *
from attacks import *
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
        Return any new sprites created as a group.
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
        self.sfxhurt = None
        self.sfxdead = None
        self.facing = "front"
        self.action = "Stand" # Stand, Walk1, Walk2
        self.image = self.images[self.ref + self.facing + self.action]
        self.anim = True # boolean, used to swap movement animations
        self.rect = self.image.get_rect()
        self.rect.topleft = pos # i.e. (0,0) or (128, 64)
        self.weapon = None # melee weapon, i.e. "wrench"
        self.gun = None # "pistol"
        self.attack = None # i.e. GroupSingle(MeleeAttack)
        self.shots = pygame.sprite.Group() # ranged attacks in motion
        self.speed = 2.5
        self.hp = 10
        self.str = 0 # Strength, melee damage
        self.dex = 0 # Dexterity, ranged damage
                     # if str (dex) == 0 then cannot attack
        self.item = None # item dropped if killed
        self.dropchance = 50 # percent chance that items will drop
        self.brain = VillagerBrain(self)
        self.moving = False
        self.attacked = False # reset each frame, acts as a "danger sense"
        self.flinchtimermax = FLINCHTIMER
        self.flinchtimer = 0
        self.animtimermax = ANIMATETIMER
        self.animtimer = 0 # increment to timermax, then reset to 0
        self.stuntimermax = ANIMATETIMER
        self.stuntimer = 0 # increment to stuntimermax then reset to 0
        self.attacktimermax = WAITTIMER
        self.attacktimer = 0 # increments to attacktimermax, then reset to 0
        # can only attack if attacktimer == 0

    def space_ahead(self):
        """Returns a rectangle space directly in front of the npc.
        """
        x = 0
        y = 0
        if self.facing == "front":
            y = self.rect.height
        elif self.facing == "back":
            y = -self.rect.height
        elif self.facing == "left":
            x = -self.rect.width
        elif self.facing == "right":
            x = self.rect.width
        return self.rect.move(x,y)

    def mattack(self):
        """Execute a melee attack.
        Returns the new attack.
        """
        if self.attacktimer <> 0:
            return pygame.sprite.Group()
        sfxPlay("meleemiss.wav")
        self.action = "Attack"
        self.attacktimer = 1
        self.attack = pygame.sprite.GroupSingle(
            MeleeAttack(self, self.weapon, self.images))
        return self.attack

    def rattack(self):
        """Execute a ranged attack, based on the mouse pos.
        Returns the new attack.
        """
        if self.attacktimer <> 0:
            return pygame.sprite.Group()
        self.action = "Attack"
        self.attacktimer = 1
        self.attack = pygame.sorite.GroupSingle(
            RangedAttack(self, self.gun, self.images))
        (x, y) = pygame.mouse.get_pos()
        newshot = Shot("bullet", self.images, self, (x,y))
        self.shots.add(newshot)
        newsprites = pygame.sprite.Group((self.attack, newshot))
        return newsprites

    def hit(self, damage):
        """Just got attacked.
        Returns True if the attack hits, else False.
        """
        if self.flinchtimer > 0:
            return False
        self.flinchtimer = 1
        self.attacked = True
        self.hp -= damage
        if self.hp < 1:
            if self.attack is not None:
                self.attack.sprite.kill()
            for shot in self.shots:
                shot.kill()
            self.die()
            sfxPlay(self.sfxdead)
        else:
            sfxPlay(self.sfxhurt)
        return True

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

    def animate(self):
        """Determines the current image to use and assigns it to self.image
        action = "Stand", "Walk1", etc
        """
        if self.action is not None:
            # update image and reset timer
            self.image = self.images[self.ref + self.facing + self.action]
            return
        if self.attack is not None and self.attack.sprite.timer > 0:
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

    def tick(self):
        """Update variables independent of subclass.
        Call this at the start of each update.
        Return False if stunned (do not continue turn)
        """
        # update timers
        if self.flinchtimer == self.flinchtimermax:
            self.flinchtimer = 0
        elif self.flinchtimer > 0:
            self.flinchtimer += 1
        if self.attacktimer == self.attacktimermax:
            self.attacktimer = 0
        elif self.attacktimer > 0:
            self.attacktimer += 1
        # check stun timer
        if self.stuntimer > 0:
            if self.stuntimer == self.stuntimermax:
                self.stuntimer = 0
                return False
            self.stuntimer += 1
            return newsprites
        # reset variables
        self.moving = False
        self.action = None
        return True

    def update(self, solidSprites):
        """Process actions for the sprite each frame,
        Includes AI directives and animations.
        Returns a group of new sprites, maybe empty.
        """
        self.tick()
        newsprites = self.brain.think(solidSprites)
        self.animate()
        self.attacked = False
        return newsprites

    def die(self):
        """The sprite had died.
        Returns dropped item, or None if no item is dropped.
        """
        self.kill()
        pass

