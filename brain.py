from states import *

class Brain:
    """Collection of States that transitions between them
    """
    def __init__(self, npc):
        self.states = {}
        self.activeState = None
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
    of the game loop
    """
    def think(self, spriteGroup):
        if self.activeState is None:
            return
        self.activeState.doActions(spriteGroup)
        newStateName = self.activeState.checkConditions()
        if newStateName is not None:
            self.setState(newStateName)

class VillagerBrain(Brain):
    """AI for villager, enables wandering and waiting
    """
    def __init__(self, npc):
        Brain.__init__(self, npc)
        self.addState(Wandering())
        self.addState(Waiting())
        self.setState("waiting")



    
