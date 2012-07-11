# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2

from constants import *
from vector import Vector
from math import fabs
import pygame
from random import seed, randrange, choice

MINTIME = 30 # time for moving or waiting
MAXTIME = 120

"""need ai.py to be file for generic superclass of state/state machine.
seperate py file for each state machine.
there might be a better way.
"""

class State:
    """AI behavior state (i.e. roaming, sniping, fighting, fleeing)
    """
    def __init__(self, name, npc):
        self.name = name #identifying name of the state
        self.npc = npc #npc this state is working on

    """Actions performed each frame
    Return False if the action fails, else True
    """
    def doActions(self, spriteGroup):
        pass

    """Check to see if another state should be entered
    Return string name of the new state, else None
    """
    def checkConditions(self, spriteGroup):
        pass

    """Actions to perform when this state is entered.
    Modifies npc variables.
    """
    def entryActions(self, spriteGroup):
        pass

    """Actions to perform when before exiting this state.
    modifies npc variables.
    """
    def exitActions(self, spriteGroup):
        pass

class Wandering(State):
    """Wander from point to point on the screen
    """
    def __init__(self, npc):
        State.__init__(self, "wandering", npc)
        self.timer = None # int frame count
        self.directions = {(0.0, -1.0):"back", # north
                           (0.0, 1.0):"front", # south
                           (1.0, 0.0):"right", # east
                           (-1.0, 0.0):"left", # west
                           (DIAGONAL, -DIAGONAL):"back", # ne
                           (DIAGONAL, DIAGONAL):"front", # se
                           (-DIAGONAL, DIAGONAL):"front", # sw
                           (-DIAGONAL, -DIAGONAL):"back"} # nw
        self.vector = None

    def doActions(self, group):
        """Attempt to move the npc
        Return False if the move is blocked
        """
        distance = self.vector * self.npc.speed
        newrect = self.npc.rect.move(*distance.as_tuple())
        if newrect.bottom > CENTERYEND:
            return False
        elif newrect.top < CENTERYSTART:
            return False
        elif newrect.left < CENTERXSTART:
            return False
        elif newrect.right > CENTERXEND:
            return False
        for s in group:
            if newrect.colliderect(s.rect) and self.npc.name is not s.name:
                return False
        self.npc.rect = newrect
        self.timer -= 1
        return True

    def checkConditions(self, group):
        """If the point has been reached, begin waiting.
        Returns the name of the new state, else None
        """
        if self.timer <= 0:
            return "waiting"
        else:
            return None

    def entryActions(self, group):
        seed()
        self.npc.moving = True
        self.timer = randrange(MINTIME, MAXTIME)
        heading = choice(self.directions.keys())
        self.vector = Vector(*heading)
        self.npc.facing = self.directions[heading]
        #setRandomDestination(self.npc, group)

    def exitActions(self, group):
        self.npc.moving = False
        self.npc.vector = None

class Waiting(State):
    """Wait for a random number of frames
    """
    def __init__(self, npc):
        State.__init__(self, "waiting", npc)
        self.timer = 0

    def doActions(self, group):
        self.timer -= 1
        return True

    def checkConditions(self, group):
        if self.timer < 0:
            return "wandering"
        else:
            return None

    def entryActions(self, Group):
        self.npc.moving = False
        seed()
        self.timer = randrange(MINTIME, MAXTIME)

    def exitActions(self, Group):
        pass

# Helper functions

#deprecated

def validPath(sprite, solidGroup, destpoint):
    """Check to see if there is a straight path to the target tuple
    Returns True if valid, else False
    """
    valid = True
    testrect = sprite.rect.copy()
    vector = Vector.from_points((testrect.centerx, testrect.centery), destpoint)
    vector = vector.normalize() * 10
    distance = Vector.from_points(testrect.center, destpoint).get_magnitude()
    while (valid and distance > 20):
        testrect.move_ip(vector.x, vector.y)
        for sprite in solidGroup:
            if testrect.colliderect(sprite.rect):
                valid = False
                continue
        # set up loop testing condition: distance to destination
        distance = Vector.from_points(testrect.center, destpoint).get_magnitude()
    return valid

#deprecated
def setRandomDestination(npc, solidGroup):
    """Helper function to find a valid (oocupyable) point on the map.
    Modifies npc's destination, vector.
    """
    collision = True
    while collision:
        dest = (randrange(CENTERXSTART, CENTERXEND),
                randrange(CENTERYSTART, CENTERYEND))
        for sprite in solidGroup:
            if sprite.rect.collidepoint(dest):
                break # from for loop
        collision = not validPath(npc, solidGroup, dest)
    npc.destination = dest
    npc.vector = Vector(dest[0]-npc.rect.centerx,
                        dest[1]-npc.rect.centery).normalize()

#deprecated
def move(npc, solidGroup):
    """Attempt to move the npc based on its vector.
    Return False if the move fails, else True
    """
    if npc.vector is not None:
        distance = npc.vector * npc.speed
        newrect = npc.rect.move(*distance.as_tuple())
        for solidsprite in solidGroup:
            if newrect.colliderect(solidsprite.rect):
                if solidsprite == npc:
                    continue
                return False
        npc.rect = newrect
        return True
