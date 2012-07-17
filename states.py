# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from constants import *
import globalvars
from vector import Vector
from math import fabs
import pygame
from random import seed, randrange, choice

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

    def doActions(self):
        """Actions performed each frame.
        Throws AIError if the action fails.
        """
        pass

    def checkConditions(self):
        """Check to see if another state should be entered
        Return string name of the new state, else None
        """
        pass

    def entryActions(self):
        """Actions to perform when this state is entered.
        Modifies npc variables.
        """
        pass

    def exitActions(self):
        """Actions to perform when before exiting this state.
        modifies npc variables.
        """
        pass

class Wandering(State):
    """Wander from point to point on the screen.
    Transitions to/from: waiting.
    If nextstate is specified, it will go to that.
    """
    def __init__(self, npc, nextstate=None):
        State.__init__(self, "wandering", npc)
        self.nextstate = nextstate

    def doActions(self):
        """Attempt to move the npc
        Throws AIError if the move fails
        """
        if self.npc.move(self.vector) <> "success":
            raise AIError(self.npc.name+" wandering move failed.")
        self.timer -= 1
        return

    def checkConditions(self):
        """If the point has been reached, begin waiting.
        Returns the name of the new state, else None
        New state is waiting by default, unless specified
        """
        state = self.nextstate
        if state is None:
            state = "waiting"
        global solidGroup
        if self.timer <= 0:
            return state
        spaceahead = (self.vector * TILESIZE).as_tuple()
        newrect = self.npc.rect.move(*spaceahead)
        if newrect.bottom > CENTERYEND:
            return state
        elif newrect.top < CENTERYSTART:
            return state
        elif newrect.left < CENTERXSTART:
            return state
        elif newrect.right > CENTERXEND:
            return state
        for s in globalvars.solidGroup:
            if newrect.colliderect(s.rect) and self.npc.name is not s.name:
                return state
        return None

    def entryActions(self):
        global solidGroup
        seed()
        self.npc.moving = True
        self.timer = randrange(MINTIME, MAXTIME)
        heading = None
        while heading is None:
            heading = choice(self.directions.keys())
            self.vector = Vector(*heading).normalize()
            nextvect = self.vector * TILESIZE
            nextrect = self.npc.rect.move(*nextvect.as_tuple())
            for s in globalvars.solidGroup:
                if s.name is not self.npc.name and nextrect.colliderect(s.rect):
                    heading = None
                    break
        #self.npc.facing = self.directions[heading]

    def exitActions(self):
        self.npc.moving = False

class Waiting(State):
    """Wait for a random number of frames.
    Transitions: wandering
    """
    def __init__(self, npc):
        State.__init__(self, "waiting", npc)
        self.timer = 0

    def doActions(self):
        """Countdown the wait timer.
        Does not throw AIException because it cannot fail.
        """
        self.timer -= 1
        return

    def checkConditions(self):
        """Returns wandering if time is over, else None.
        """
        if self.timer < 0:
            return "wandering"
        else:
            return None

    def entryActions(self):
        """Set up random amount of time to wait.
        """
        self.npc.moving = False
        seed()
        self.timer = randrange(MINTIME, MAXTIME)

    def exitActions(self):
        """No actions needed.
        """
        pass

class Seeking(State):
    """Move toward the hero, getting within attack range.
    Transitions: attacking"""
    def __init__(self, npc):
        State.__init__(self, "seeking", npc)
        #global hero
        self.target = globalvars.hero

    def doActions(self):
        """Move toward the hero.
        Raise AIAlert if the move fails."""
        dest = self.target.rect.center
        vect = Vector.from_points(self.npc.rect.center, dest).normalize()
        if self.npc.move(vect) <> "success":
            raise AIError(self.npc.name+" seeking move failed.")
        return

    def checkConditions(self):
        """If the hero is within range, return "attacking"."""
        #global hero
        range = self.npc.space_ahead()
        if range.colliderect(globalvars.hero.rect):
            return "attacking"
        return None

    def entryActions(self):
        pass


class Attacking(State):
    """Moving toward the hero and attacking.
    Transitions: seeking
    """
    def __init__(self, npc):
        State.__init__(self, "attacking", npc)
        
    def doActions(self):
        """Attack the hero when possible."""
        #global hero
        reach = self.npc.space_ahead()
        if reach.colliderect(globalvars.hero.rect):
            self.npc.mattack()

    def checkConditions(self):
        """If the hero moves out of range, change to seeking.
        Returns the name "seeking" if the hero is out of range"""
        #global hero
        reach = self.npc.space_ahead()
        if not reach.colliderect(globalvars.hero.rect):
            return "seeking"
        return None

    def entryActions(self):
        pass
