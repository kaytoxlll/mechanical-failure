# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from math import fabs
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
    def __init__(self, name, reference, pos, solid):
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

    def hit(self, attack, frompoint):
        """Just got hit by an attack.
        Return True if the attack hit.
        """
        if self.solid:
            return True
        return False

class NPC(pygame.sprite.Sprite):
    """Base sprite class for characters.
    Sprite class for civilians
    """
    def __init__(self, name, reference, pos): #pos = (x,y), images = dictionary 
        pygame.sprite.Sprite.__init__(self)
        global images
        self.name = name # i.e. Bob
        self.ref = reference # i.e. VillagerMan
        self.sfxhurt = None
        self.sfxdead = None
        self.facing = "front"
        self.action = "Stand" # Stand, Walk1, Walk2
        self.image = images[self.ref + self.facing + self.action]
        self.anim = True # boolean, used to swap movement animations
        self.rect = self.image.get_rect()
        self.rect.topleft = pos # i.e. (0,0) or (128, 64)
        self.weapon = None # melee weapon, i.e. "wrench"
        self.gun = None # "pistol"
        self.attack = None # i.e. MeleeAttack()
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
        self.guntimermax = GUNTIMER
        self.guntimer = 0
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
        Adds the attack to the attackQ
        """
        global attackQ
        if self.attacktimer <> 0:
            return
        sfxPlay("meleemiss.wav")
        self.action = "Attack"
        self.attacktimer = 1
        self.attack = MeleeAttack(self, self.weapon)
        attackQ.add(self.attack)
        return

    def rattack(self):
        """Execute a ranged attack, based on the mouse pos.
        Adds the attack to the attackQ
        """
        global attackQ
        if self.guntimer <> 0:
            return
        # update facing to match shooting direction
        (x,y) = pygame.mouse.get_pos()
        if fabs(self.rect.centerx-x) > fabs(self.rect.centery-y):
            if x < self.rect.centerx:
                self.facing = "left"
            else:
                self.facing = "right"
        else:
            if y < self.rect.centery:
                self.facing = "back"
            else:
                self.facing = "front"
        sfxPlay("shotgun.wav")
        self.action = "Attack"
        self.guntimer = 1
        self.attack = RangedAttack(self, self.gun)
        newshot = Shot(self, "bullet", (x,y))
        attackQ.add(self.attack)
        attackQ.add(newshot)
        return

    def hit(self, attack, frompoint):
        """Just got attacked.
        Returns True if the attack hit, else False
        """
        if self.flinchtimer > 0:
            return False
        self.hp -= attack.damage
        if self.hp < 1:
            self.die()
            sfxPlay(self.sfxdead)
        else:
            self.flinchtimer = 1
            self.attacked = True
            sfxPlay(self.sfxhurt)
            vect = Vector.from_points(frompoint, self.rect.center)
            self.knockback(vect, attack)
        return True

    def knockback(self, vector, attack, velocity=KNOCKBACK):
        """Push the npc back until it hits a solid object.
        """
        global solidGroup
        if vector is None or (vector.x==0.0 and vector.y==0.0):
            return
        vector.normalize()
        distance = vector * velocity
        for i in range(velocity):
            newrect = self.rect.move(*distance.as_tuple())
            if newrect.bottom > CENTERYEND:
                break
            elif newrect.top < CENTERYSTART:
                break
            elif newrect.left < CENTERXSTART:
                break
            elif newrect.right > CENTERXEND:
                break
            collision = False
            for s in solidGroup:
                if newrect.colliderect(s.rect) and \
                   self.name is not s.name and s.name is not attack.name:
                    collision = True
                    break
            if collision == True:
                break
            self.rect = newrect

    def move(self, vector, velocity=None):
        """Attempt to move the sprite based on the vector.
        Modifies the moving flag accordingly.
        If there is a collision with the solid sprites or the map edge,
        return "success", else return the name of the collided-with object.
        This could also be an edge, i.e. "west" for the left edge of the screen.
        """
        global solidGroup
        if vector is None or (vector.x==0.0 and vector.y==0.0):
            # no distance to move
            self.moving = False
            return "success" 
        distance = vector * self.speed
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
        for s in solidGroup:
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
        global images
        if self.action is not None:
            # update image and reset timer
            self.image = images[self.ref + self.facing + self.action]
            return
        if self.attack is not None and self.attack.timer > 0:
            return
        if self.animtimer == self.animtimermax and self.moving == True:
            # full timer (1/1), update walk animation
            if self.anim:
                self.image = images[self.ref + self.facing + "Walk1"]
            else:
                self.image = images[self.ref + self.facing + "Walk2"]
            self.anim = not self.anim
        elif self.animtimer == self.animtimermax / 2 and self.moving:
            # half timer (0.5/1), update stand animation
            self.image = images[self.ref + self.facing + "Stand"]
        elif self.moving == False:
            self.image = images[self.ref + self.facing + "Stand"]

    def tick(self):
        """Update variables independent of subclass.
        Call this at the start of each update.
        Return False if stunned (do not continue turn)
        """
        # update timers
        if self.animtimer == self.animtimermax:
            self.animtimer = 0
            self.action = None
        else:
            self.animtimer += 1
        if self.flinchtimer == self.flinchtimermax:
            self.flinchtimer = 0
        elif self.flinchtimer > 0:
            self.flinchtimer += 1
        if self.attacktimer == self.attacktimermax:
            self.attacktimer = 0
        elif self.attacktimer > 0:
            self.attacktimer += 1
        if self.guntimer == self.guntimermax:
            self.guntimer = 0
        elif self.guntimer > 0:
            self.guntimer += 1
        # check stun timer
        if self.stuntimer > 0:
            self.stuntimer += 1
            if self.stuntimer == self.stuntimermax:
                self.stuntimer = 0
            else:
                return False
        # reset variables
        self.moving = False
        return True

    def update(self):
        """Process actions for the sprite each frame,
        Includes AI directives and animations.
        """
        self.tick()
        self.brain.think()
        self.animate()
        self.attacked = False
        return

    def die(self):
        """The sprite had died.
        Updates backgroundQ with blood.
        """
        global backgroundQ
        # kill attack
        if self.attack is not None:
            self.attack.sprite.kill()
        backgroundQ.add(Obstacle("blood1", "terrain", self.rect.topleft, False))
        self.kill()

