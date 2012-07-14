# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

"""To do:
work on shot
"""

from constants import *
from vector import Vector
from sprites import *
import pygame

class Attack(pygame.sprite.Sprite):
    """Sprite for an attack, such as a sword swing or gunshot.
    Used for unarmed attacks (punching and biting, for animals)
    """
    def __init__(self, npc, reference=None, images=None):
        pygame.sprite.Sprite.__init__(self)
        self.name = npc.name # prevents collision when moving
        self.ref = reference # i.e. wrench
        #self.images = images
        self.image = pygame.Surface((1,1))
        self.image.set_alpha(0)
        self.rect = npc.space_ahead()
        self.damage = npc.str
        self.npc = npc
        self.timermax = ATTACKTIMER
        self.timer = 0 # counts up to timermax, then attack is over

    def update(self, solidSprites):
        """Align the attack with the npc's rect,
        See if it hit anyone, and process the hit.
        """
        if self.timer == self.timermax:
            # if the attack is over, kill it
            self.npc.attack = None
            self.kill()
            return
        # update position
        self.rect = self.npc.space_ahead()
        # check for collisions
        hitlist = pygame.sprite.spritecollide(self, solidSprites, False)
        for s in hitlist:
            if s.name is not self.name:
                s.hit(self.damage)
        # update timer
        self.timer += 1
        self.animate()

    def animate(self):
        """Change the weapons current image.
        This default attack has no image.
        """
        self.image.set_alpha(0)

    def hit(self, damage):
        """This attack has been hit by another attack.
        All of this game's sprites need this.
        """
        pass

class MeleeAttack(Attack):
    def __init__(self, npc, reference, images):
        Attack.__init__(self, npc, reference, images)
        self.images = images
        if reference <> None:
            self.image = images[reference + npc.facing + "1"] # i.e. wrenchfront1

        
    def animate(self):
        """Update the swinging animation.
        """
        if self.timer == 5: # 1/2 max
            self.image = self.images[self.ref + self.npc.facing + "2"]

class RangedAttack(Attack):
    """Basically holding a gun in front of you.
    """
    def __init__(self, npc, reference, images):
        Attack.__init__(self, npc, reference, images)
        self.image = images[reference + npc.facing]

    def update(self, solidSprites):
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
        timer += 1
        self.animate()

    def animate(self):
        """Put the gun away when the attack ends.
        """
        pass

class Shot(pygame.sprite.Sprite):
    """Sprite for a projectile, like a bullet.
    """
    def __init__(self, npc, reference, images, dest):
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.vector = Vector.from_points(npc.rect.center, dest).normalize()
        self.speed = 5
        self.image = images["ammo" + reference]
        self.rect = self.image.get_rect()
        x, y = 0
        # start the shot in the center of the tile in front of the npc
        if npc.facing == "front":
            y = TILESIZE
        elif npc.facing == "back":
            y = -TILESIZE
        elif npc.facing == "left":
            x = -TILESIZE
        elif npc.facing == "right":
            x = TILESIZE
        self.rect.center = (npc.rect.centerx + x, npc.rect.centery + y)

    def update(self, solidSprites):
        """Move the shot and handle collisions.
        """
        distance = self.vector * self.speed
        self.rect.move_ip(*distance.as_tuple())
        for s in pygame.sprite.spritecollide(self, solidSprites):
            # handle the first target hit by the shot
            s.hit(self.damage)
            self.kill()
            return
        if self.rect.bottom > CENTERYEND or \
        self.rect.top < CENTERYSTART or \
        self.rect.left < CENTERXSTART or \
        self.rect.right > CENTERXEND:
            self.kill()

    def hit(self, damage=0):
        """This shot got hit by an attack.
        """
        self.kill()

