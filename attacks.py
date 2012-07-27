# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

"""To do:

"""

from constants import *
import globalvars
from vector import Vector
import menu
import sprites
import pygame

class BasicAttack(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Attack(BasicAttack):
    """Sprite for an attack, such as a sword swing or gunshot.
    """
    def __init__(self, npc):
        BasicAttack.__init__(self)
        self.name = npc.name # prevents collision when moving
        #self.ref # i.e. wrench
        self.rect = npc.space_ahead()
        #self.damage
        self.npc = npc
        self.timermax = ATTACKTIMER
        self.timer = 0 # counts up to timermax, then attack is over
        self.hit = False # flag for hit detection, to prevent multihits

    def examine(self):
        """PC examined, don't do anything."""
        return True

    def update(self):
        """Align the attack with the npc's rect,
        See if it hit anyone, and process the hit.
        """
        #global solidGroup
        if self.timer == self.timermax:
            # if the attack is over, kill it
            self.npc.attack = None
            self.kill()
            return
        # update position
        self.rect = self.npc.space_ahead()
        # check for collisions
        if self.hit == False:
            hitlist = pygame.sprite.spritecollide(self, globalvars.solidGroup, False)
            for s in hitlist:
                if s.name is not self.name and not issubclass(type(s), BasicAttack):
                    hitval = s.hit(self, self.npc.rect.center)
                    if hitval:
                        self.hit = True
                        sfxPlay("meleehit.wav")
                        break
        # update timer
        self.timer += 1
        self.animate()
        return

    def hit(self, attack, frompoint):
        return False

    def animate(self):
        """Change the weapons current image.
        This default attack has no image.
        """
        pass

    def hit(self, attack, frompoint):
        """This attack has been hit by another attack.
        All of this game's sprites need this.
        Return False because attacks pass through each other
        """
        return False

class MeleeAttack(Attack):
    def __init__(self, npc, reference=None):
        Attack.__init__(self, npc)
        #global images
        self.ref = reference
        self.damage = npc.str
        if self.ref is None:
            self.image = pygame.Surface((TILESIZE, TILESIZE))
            self.image.set_alpha(0)
        else:
            self.image = globalvars.images[self.ref + npc.facing + "1"] # i.e. wrenchfront1
        
    def animate(self):
        """Update the swinging animation and sound.
        """
        #global images
        if self.ref is not None:
            if self.timer >= self.timermax/2 and self.ref is not None:
                # 1/2 max
                self.image = globalvars.images[self.ref + self.npc.facing + "2"]
            else:
                self.image = globalvars.images[self.ref + self.npc.facing + "1"]

class RangedAttack(Attack):
    """Basically holding a gun in front of you.
    """
    def __init__(self, npc, reference):
        Attack.__init__(self, npc)
        #global images
        self.ref = reference
        self.image = globalvars.images[reference + npc.facing]

    def update(self):
        """Don't worry about hit detection, just time the attack.
        """
        if self.timer == self.timermax:
            # if the attack is over, kill it
            self.npc.attack = None
            self.kill()
            return
        # update position
        self.rect = self.npc.space_ahead()
        # update timer
        self.timer += 1
        self.animate()

    def animate(self):
        """Move the gun with the npc's facing
        """
        #global images
        self.image = globalvars.images[self.ref + self.npc.facing]

class Bomb(BasicAttack):
    """Sprite for a bomb about to explode"""
    def __init__(self, npc):
        BasicAttack.__init__(self)
        self.npc = npc
        self.name = npc.name
        self.damage = 0
        self.image = globalvars.images["ammo" + "bomb1"]
        self.rect = self.image.get_rect()
        self.rect.center = npc.space_ahead().center
        self.timermax = 60 # frames
        self.timer = 0 # count up to timermax, change image each 10

    def examine(self):
        menu.dialogue("It's about to explode!")
        return True

    def update(self):
        """Increment timer, changing image each 10 frames.
        When timer reaches max, create Explosion.
        """
        if self.timer == 20:
            self.image = globalvars.images["ammo" + "bomb2"]
        elif self.timer == 40:
            self.image = globalvars.images["ammo" + "bomb3"]
        elif self.timer >= self.timermax:
            sfxPlay("explosion.wav")
            self.kill()
            globalvars.attackQ.add(Explosion(self))
        self.timer += 1

    def hit(self, attack, frompoint):
        """detonate now"""
        self.timer = self.timermax
        return True

class Explosion(BasicAttack):
    """Explosion from a bomb"""
    def __init__(self, bomb):
        BasicAttack.__init__(self)
        self.name = "explosion"
        self.damage = 10
        self.image = globalvars.images["ammo" + "explosion1"]
        self.rect = self.image.get_rect()
        self.rect.center = bomb.rect.center
        self.timermax = 10
        self.timer = 0

    def examine(self):
        return True

    def update(self):
        for s in pygame.sprite.spritecollide(self, globalvars.solidGroup, False):
            if isinstance(s, sprites.NPC):
                s.hit(self, self.rect.center, knockback=10)
            elif type(s) is sprites.Explodeable:
                s.kill()
            elif type(s) is sprites.Obstacle and s.breakable == True:
                s.hit(self, self.rect.center)
        if self.timer == 5:
            self.image = globalvars.images["ammo" + "explosion2"]
        elif self.timer == self.timermax:
            self.kill()
        self.timer += 1

    def hit(self, attack, frompoint):
        return False

class Shot(BasicAttack):
    """Sprite for a projectile, like a bullet.
    """
    def __init__(self, npc, reference, dest):
        BasicAttack.__init__(self)
        #global images
        self.npc = npc
        self.name = npc.name
        self.damage = npc.dex
        self.vector = Vector.from_points(npc.rect.center, dest).normalize()
        self.speed = 15
        self.image = globalvars.images["ammo" + reference]
        self.rect = self.image.get_rect()
        x = 0
        y = 0
        # start the shot in the center of the tile in front of the npc
        startrect = npc.space_ahead()
        self.rect.center = startrect.center

    def examine(self):
        """PC examines, don't do anything."""
        return True

    def update(self):
        """Move the shot and handle collisions.
        """
        #global solidGroup
        distance = self.vector * self.speed
        self.rect.move_ip(*distance.as_tuple())
        for s in pygame.sprite.spritecollide(self, globalvars.solidGroup, False):
            # handle the first target hit by the shot
            if s.name is not self.name and not issubclass(type(s), BasicAttack):
                if isinstance(s, sprites.Obstacle) and s.solid is False:
                    continue
                s.hit(self, self.npc.rect.center)
                self.kill()
                return
        if self.rect.bottom > CENTERYEND or \
        self.rect.top < CENTERYSTART or \
        self.rect.left < CENTERXSTART or \
        self.rect.right > CENTERXEND:
            self.kill()

    def hit(self, attack, frompoint):
        """This shot got hit by an attack.
        """
        self.kill()
        return True

