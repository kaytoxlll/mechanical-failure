# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

"""To do:

"""

from constants import *
import globalvars
from vector import Vector
import sprites
import pygame

class Attack(pygame.sprite.Sprite):
    """Sprite for an attack, such as a sword swing or gunshot.
    """
    def __init__(self, npc):
        pygame.sprite.Sprite.__init__(self)
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
                if s.name is not self.name and not issubclass(type(s), Attack):
                    hitval = s.hit(self, self.npc.rect.center)
                    if hitval:
                        self.hit = True
                        sfxPlay("meleehit.wav")
                        break
        # update timer
        self.timer += 1
        self.animate()
        return

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
            self.image = pygame.Surface((TILESIZE,TILESIZE))
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

class Shot(pygame.sprite.Sprite):
    """Sprite for a projectile, like a bullet.
    """
    def __init__(self, npc, reference, dest):
        pygame.sprite.Sprite.__init__(self)
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
            if s.name is not self.name and not issubclass(type(s), Attack):
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

