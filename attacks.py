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
    def __init__(self, reference=None, images=None, npc):
        pygame.sprite.Sprite__init__(self)
        self.ref = reference # i.e. wrench
        #self.images = images
        #self.image = None
        self.rect = npc.space_ahead()
        self.damage = npc.str
        self.npc = npc
        self.timermax = 10
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
        hitlist = pygame.sprite.spritecollide(self, solidSprites)
        for s in hitlist:
            s.hit(self.damage)
        # update timer
        timer += 1
        self.animate()

    def animate(self):
        """Change the weapons current image.
        This default attack has no image.
        """
        pass

    def hit(self, damage):
        """This attack has been hit by another attack.
        All of this games sprites need this.
        """
        pass

class MeleeAttack(Attack):
    def __init__(self, reference, images, npc):
        Attack.__init__(self, reference, images, npc)
        self.image = images[reference + npc.facing + "1"] # i.e. wrenchfront1
        
    def animate(self):
        """Update the swinging animation.
        """
        if self.timer == 5: # 1/2 max
            self.image = self.images[self.ref + self.npc.facing + "2"]

class RangedAttack(Attack):
    """Basically holding a gun in front of you.
    """
    def __init__(self, reference, images, npc):
        Attack.__init__(self, reference, images, npc)
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
    """Sprite for a projectile, like a bullet or grenade
    """
    def __init__(self, reference, images, npc, vector, speed=5, time=999):
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.vector = vector.normalize()
        self.speed = speed
        self.time = time
        self.image = images["ammo" + reference]
        self.rect = self.image.get_rect()
        self.rect.center = (npc.rect.centerx + self.vector.x*TILESIZE, 
                            npc.rect.centery + self.vector.y*TILESIZE)
        

