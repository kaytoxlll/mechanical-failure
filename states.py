# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
from vector import Vector
from math import fabs
import pygame
from random import seed, randrange, choice

MINTIME = 30 # time for moving or waiting (sort of like a 'turn')
MAXTIME = 120

"""need ai.py to be file for generic superclass of state/state machine.
seperate py file for each state machine.
there might be a better way.
"""

class State:
    def __init__(self, name, npc):
        """AI behavior state (i.e. roaming, sniping, fighting, fleeing)
        """
        self.name = name #identifying name of the state
        self.npc = npc #npc this state is working on

    def doActions(self, spriteGroup):
        """Actions performed each frame.
        Returns sprite group of new sprites, possible empty
        Throws AIError if the action fails.
        """
        pass

    def checkConditions(self, spriteGroup):
        """Check to see if another state should be entered
        Return string name of the new state, else None
        """
        pass

    def entryActions(self, spriteGroup=None):
        """Actions to perform when this state is entered.
        Modifies npc variables.
        """
        pass

    def exitActions(self, spriteGroup):
        """Actions to perform when before exiting this state.
        modifies npc variables.
        """
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
        Returns an empty group.
        Throws AIError if the move fails
        """
        if self.npc.move(self.vector, group) <> "success":
            raise AIError(self.npc.name+" wandering move failed.")
        self.timer -= 1
        return pygame.sprite.Group()

    def checkConditions(self, group):
        """If the point has been reached, begin waiting.
        Returns the name of the new state, else None
        """
        if self.timer <= 0:
            return "waiting"
        spaceahead = (self.vector * TILESIZE).as_tuple()
        newrect = self.npc.rect.move(*spaceahead)
        if newrect.bottom > CENTERYEND:
            return "waiting"
        elif newrect.top < CENTERYSTART:
            return "waiting"
        elif newrect.left < CENTERXSTART:
            return "waiting"
        elif newrect.right > CENTERXEND:
            return "waiting"
        for s in group:
            if newrect.colliderect(s.rect) and self.npc.name is not s.name:
                return "waiting"
        return None

    def entryActions(self, group):
        seed()
        self.npc.moving = True
        self.timer = randrange(MINTIME, MAXTIME)
        heading = choice(self.directions.keys())
        self.vector = Vector(*heading).normalize()
        self.npc.facing = self.directions[heading]

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
        """Countdown the wait timer.
        Returns an empty group.
        Does not throw AIException because it cannot fail.
        """
        self.timer -= 1
        return pygame.sprite.Group()

    def checkConditions(self, group):
        if self.timer < 0:
            return "wandering"
        else:
            return None

    def entryActions(self, Group=None):
        self.npc.moving = False
        seed()
        self.timer = randrange(MINTIME, MAXTIME)

    def exitActions(self, Group):
        pass
