# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from math import fabs
import globalvars
import menu
from constants import *
from menu import *
from vector import Vector
from brain import *
from attacks import *
import pygame
import random

"""To do:

"""

class Obstacle(pygame.sprite.Sprite):
    """Base sprite class for map objects (i.e. barrels, etc)
    """
    def __init__(self, name, reference, pos=(0,0), solid=True, breakable=False):
        pygame.sprite.Sprite.__init__(self)
        #global images
        self.ref = reference # i.e. terrain (directory)
        self.text = []
        self.name = name # i.e. barrel (file name)
        self.image = globalvars.images[self.ref + self.name]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos # i.e. (0,0) or (128, 64)
        self.solid = solid # boolean
        self.breakable = breakable

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
            if self.breakable:
                self.kill()
                globalvars.backgroundQ.add(Obstacle("rubbish", "terrain", self.rect.topleft, solid=False))
            return True
        return False

    def examine(self):
        """PC examined this, don't do anything."""
        if self.breakable:
            menu.dialogue("This looks kinda shoddy...")
        if self.name == "vendingmachine":
            newrect = self.rect.move(0, -TILESIZE)
            for s in globalvars.solidGroup:
                if s is not self and newrect.colliderect(s.rect):
                    return s.examine()
        elif self.name == "counter":
            for s in globalvars.solidGroup:
                if s is not self and self.rect.colliderect(s.rect):
                    return s.examine()
        return True

class Floor(Obstacle):
    def __init__(self, name, reference, pos=(0,0), solid=False):
        Obstacle.__init__(self, name, reference, pos, solid)

class Transition(Obstacle):
    """Like a ladder or manhole"""
    def __init__(self, name, reference, direction, pos=(0,0), solid=False):
        Obstacle.__init__(self, name, reference, pos, solid)
        self.direction = direction # "up" or "down"

    def examine(self):
        if self.name == "ladderup":
            return menu.dialogue("Climb up?")
        elif self.name == "ladderdown":
            return menu.dialogue("Climb down?")

class Sign(Obstacle):
    """Like an obstacle, but with a message"""
    def __init__(self, name, reference, msg, pos=(0,0), solid=True):
        Obstacle.__init__(self, name, reference, pos, solid)
        self.message = msg

    def examine(self):
        menu.dialogue(self.message)

class Moveable(Obstacle):
    """Obstacle that can be removed by a script"""
    def __init__(self, name, reference, pos=(0,0), solid=True):
        Obstacle.__init__(self, name, reference, pos, solid)

    def examine(self):
        return menu.dialogue("This door is shut tight...")

class Locked(Obstacle):
    """Obstacle that can be removed with a key"""
    def __init__(self, name, reference, pos=(0,0), solid=True):
        Obstacle.__init__(self, name, reference, pos, solid)

    def examine(self):
        if globalvars.hero.keys < 1:
            return menu.dialogue("You need a key to open this door.")
        globalvars.hero.keys -= 1
        self.kill()

class Explodeable(Obstacle):
    """Obstacle that can be destroyed by a bomb"""
    def __init__(self, name, reference, pos=(0,0), solid=True):
        Obstacle.__init__(self, name, reference, pos, solid)

    def examine(self):
        return menu.dialogue("This wall looks weak...")        

class Item(Obstacle):
    """A coin, box of ammo, potion, etc."""
    def __init__(self, name, pos=(0,0), solid=False):
        # name i.e. "potion"
        Obstacle.__init__(self, name, "items", pos, solid)

class ShopItem(Item):
    """Like an item, but examined and bought instead of picked up"""
    def __init__(self, name, price, pos=(0,0), solid=False):
        Item.__init__(self, name, pos, solid)
        self.price = price

    def examine(self):
        """Let PC buy or decline the item"""
        bought = menu.dialogue("Buy "+str(self.name)+" for "+str(self.price)+"?")
        if bought:
            if globalvars.hero.coins >= self.price:
                globalvars.hero.coins -= self.price
                globalvars.hero.get(self)
                #self.kill()
            else:
                menu.dialogue("Not enough coins!")

class NPC(pygame.sprite.Sprite, object):
    """Base sprite class for characters.
    Sprite class for civilians
    """
    def __init__(self, name, reference, pos=(0,0), text=[]):
        pygame.sprite.Sprite.__init__(self)
        #global images
        self.name = name # i.e. Bob
        self.text = text # list of things that are said
        self.ref = reference # i.e. VillagerMan
        self.sfxhurt = None
        self.sfxdead = None
        self.facing = "front"
        self.action = "Stand" # Stand, Walk1, Walk2
        self.image = globalvars.images[self.ref + self.facing + self.action]
        self.anim = True # boolean, used to swap movement animations
        self.rect = self.image.get_rect()
        self.rect.topleft = pos # i.e. (0,0) or (128, 64)
        self.weapon = None # melee weapon, i.e. "wrench"
        self.gun = None # "pistol"
        self.ammo = 0
        self.attack = None # i.e. MeleeAttack()
        self.speed = 2.5
        self.hp = 10
        self.str = 0 # Strength, melee damage
        self.dex = 0 # Dexterity, ranged damage
                     # if str (dex) == 0 then cannot attack
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

    def examine(self):
        """PC talked to this person, show dialogue.
        Return value of last dialogue, i.e. True for 'yes'.
        """
        #global window
        answer = True
        for line in self.text:
            answer = menu.dialogue(self.name + ": " + line)
        return answer

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
        #global attackQ
        if self.attacktimer <> 0:
            return
        sfxPlay("meleemiss.wav")
        self.action = "Attack"
        self.attacktimer = 1
        self.attack = MeleeAttack(self, self.weapon)
        globalvars.attackQ.add(self.attack)
        return

    def rattack(self):
        """Execute a ranged attack, based on the mouse pos.
        Adds the attack to the attackQ
        """
        #global attackQ
        if self.guntimer <> 0:
            return
        if self.ammo < 1:
            return
        self.ammo -= 1
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
        globalvars.attackQ.add(self.attack)
        globalvars.attackQ.add(newshot)
        return

    def hit(self, attack, frompoint, knockback=5):
        """Just got attacked.
        Returns True if the attack hit, else False
        """
        if type(self) == NPC:
            return False
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
            self.knockback(vect, attack, knockback)
        return True

    def knockback(self, vector, attack, velocity=5):
        """Push the npc back until it hits a solid object.
        """
        #global solidGroup
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
            for s in globalvars.solidGroup:
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
        #global solidGroup
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
        for i in globalvars.itemGroup:
            if newrect.colliderect(i.rect) and self is globalvars.hero:
                self.get(i)
        for s in globalvars.solidGroup:
            if newrect.colliderect(s.rect) and self.name is not s.name and \
               globalvars.attackGroup.has(s) is not True:
                self.moving = False
                return s.name
        self.rect = newrect
        self.moving = True
        # update facing
        if fabs(vector.x) > fabs(vector.y): # moving more side than up/down
            if vector.x < 0:
                self.facing = "left"
            else:
                self.facing = "right"
        else:
            if vector.y < 0:
                self.facing = "back"
            else:
                self.facing = "front"
        return "success"

    def animate(self):
        """Determines the current image to use and assigns it to self.image
        action = "Stand", "Walk1", etc
        """
        #global images
        if self.action is not None:
            # update image and reset timer
            self.image = globalvars.images[self.ref + self.facing + self.action]
            return
        if self.attack is not None and self.attack.timer > 0:
            return
        if self.animtimer == self.animtimermax and self.moving == True:
            # full timer (1/1), update walk animation
            if self.anim:
                self.image = globalvars.images[self.ref + self.facing + "Walk1"]
            else:
                self.image = globalvars.images[self.ref + self.facing + "Walk2"]
            self.anim = not self.anim
        elif self.animtimer == self.animtimermax / 2 and self.moving:
            # half timer (0.5/1), update stand animation
            self.image = globalvars.images[self.ref + self.facing + "Stand"]
        elif self.moving == False:
            self.image = globalvars.images[self.ref + self.facing + "Stand"]

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

    def drop(self, itemname):
        """Place an item on the ground"""
        item = Item(itemname)
        globalvars.itemQ.add(item)
        item.rect.center = self.rect.center

    def die(self):
        """The sprite had died.
        Updates backgroundQ with blood.
        """
        #global backgroundQ
        # kill attack
        if self.attack is not None:
            self.attack.kill()
        globalvars.backgroundQ.add(Obstacle("blood1", "terrain", self.rect.topleft, False))
        self.kill()

