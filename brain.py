# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2

from states import *

class Brain:
    """Collection of States that transitions between them
    """
    def __init__(self, npc, spriteGroup):
        self.states = {}
        self.activeState = None
        self.safeState = None # when a state fails, go back to this
        self.npc = npc

    def addState(self, state):
        self.states[state.name] = state

    def setState(self, stateName, spriteGroup):
        if self.activeState is not None:
            self.activeState.exitActions(spriteGroup)
        self.activeState = self.states[stateName]
        self.activeState.entryActions(spriteGroup)

    """Handles the AI calculations and has the
    Sprite perform actions, call this each frame
    of the game loop
    """
    def think(self, spriteGroup):
        if self.activeState is None:
            return
        if self.activeState.doActions(spriteGroup) is False:
            self.setState(self.safeState.name, spriteGroup)
            return
        newStateName = self.activeState.checkConditions(spriteGroup)
        if newStateName is not None:
            self.setState(newStateName, spriteGroup)

class VillagerBrain(Brain):
    """AI for villager, enables wandering and waiting
    """
    def __init__(self, npc, spriteGroup):
        Brain.__init__(self, npc, spriteGroup)
        self.addState(Wandering(npc))
        self.addState(Waiting(npc))
        self.setState("waiting", spriteGroup)
        self.safeState = self.states["waiting"]
