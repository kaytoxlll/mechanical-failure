# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

from states import *
from constants import *

class Brain:
    """Collection of States that transitions between them
    """
    def __init__(self, npc):
        self.states = {}
        self.activeState = None
        self.safeState = None # when a state fails, go back to this
        self.npc = npc

    def addState(self, state):
        self.states[state.name] = state

    def setState(self, stateName):
        if self.activeState is not None:
            self.activeState.exitActions()
        self.activeState = self.states[stateName]
        self.activeState.entryActions()

    """Handles the AI calculations and has the
    Sprite perform actions, call this each frame
    of the game loop.
    """
    def think(self):
        if self.activeState is None:
            return
        try:
            self.activeState.doActions()
        except AIError:
            self.setState(self.safeState.name)
            return
        newStateName = self.activeState.checkConditions()
        if newStateName is not None:
            self.setState(newStateName)
        return

class VillagerBrain(Brain):
    """AI for villager, enables wandering and waiting
    """
    def __init__(self, npc):
        Brain.__init__(self, npc)
        self.addState(Wandering(npc))
        self.addState(Waiting(npc))
        self.setState("waiting")
        self.safeState = self.states["waiting"]
