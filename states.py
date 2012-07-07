from constants import *
from vector inport Vector
from math import fabs
import pygame
from random import seed, randrange

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

    def doActions(self, group):
        move(self.npc, group)

    """If the point has been reached, begin waiting.
    Returns the name of the new state, else None
    """
    def checkConditions(self, group):
        if self.npc.rect.collidepoint(self.npc.destination):
            return "waiting"
        else return None

    def entryActions(self, group):
        self.npc.moving = True
        setRandomDestination(self.npc, group)

    def exitActions(sel, group):
        self.npc.moving = False
        self.npc.vector = None
        self.npc.destination = None

class Waiting(State):
    """Wait for a random number of frames
    """
    def __init__(self, npc):
        State.__init__(self, "waiting", npc)
        self.time = None

    def doActions(self, group):
        timer -= 1

    def checkConditions(self, group):
        if timer < 0:
            return "wandering"
        else return None

    def entryActions(self, Group):
        self.npc.moving = False
        seed()
        self.timer = randrange(30, 300)

    def exitActions(self, Group):
        pass

# Helper functions


"""Checks to see if there is a straight path to the target tuple
Returns True if valid, else False
"""
def validPath(sprite, solidGroup, destpoint):
    valid = True
    testrect = sprite.rect.copy()
    vector = Vector.from_points((testrect.centerx, testrect.centery), destpoint)
    vector = vector.normalize() * 10
    while (valid and (fabs(destpoint[0] - testrect.centerx) > 30)):
        testrect.move_ip(vector.x, vector.y)
        for sprite in solidGroup:
            if testrect.colliderect(sprite.rect):
                valid = False
                continue
    return valid

"""Helper function to find a valid (oocupyable) point on the map.
Modifies npc's destination, vector.
"""
def setRandomDestination(npc, solidGroup):
    collision = True
    while collision:
        dest = (randint(CENTERXSTART, CENTERXEND),
                randint(CENTERYSTART, CENTERYEND))
        for sprite in solidGroup:
            if sprite.rect.collidepoint(dest):
                break # from for loop
        collision = not validPath(npc, solidGroup, dest)
    npc.destination = dest
    npc.vector = Vector(dest[0]-self.npc.rect.centerx,
                        dest[1]-self.npc.rect.centery).normalize()

def move(npc, solidGroup):
    """Attempt to move the npc based on its vector.
    Return False if the move fails, else True
    """
    if npc.vector is not None:
        distance = npc.vector * npc.speed
        newrect = npc.rect.move(distance)
        for solidsprite in solidGroup:
            if newrect.colliderect(solidsprite.rect):
                return False
        npc.rect = newrect
        return True
