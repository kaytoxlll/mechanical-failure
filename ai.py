from constants import *

"""
need ai.py to be file for generic superclass of state/state machine.
seperate py file for each state machine.
there might be a better way.
"""

class State:
    """AI behavior state (i.e. roaming, sniping, fighting, fleeing)"""
    def __init__(self, name, npc):
        self.name = name #identifying name of the state
        self.npc = npc #npc this state is working on

    """Checks to see if there is a straight path to the target tuple"""
    def validPath(self, solidGroup, point):
        return True

    """Helper function to find a valid (oocupyable) point on the map"""
    def setRandomDestination(self, solidGroup):
        valid = False
        while not valid:
            dest = (randint(CENTERXSTART, CENTERXEND),
                    randint(CENTERYSTART, CENTERYEND))
            valid = True
        self.npc.destination = dest
        self.npc.vector = Vector2(dest[0]-self.npc.rect.centerx,
                                  dest[1]-self.npc.rect.centery).normalize()

    """Actions performed each frame"""
    def doActions(self, spriteGroup):
        pass

    """Check to see if another state should be entered
       Return string name of the new state, else None"""
    def checkConditions(self, spriteGroup):
        pass

    """Actions to perform when this state is entered"""
    def entryActions(self, spriteGroup):
        pass

    """Actions to perform when before exiting this state"""
    def exitActions(self, spriteGroup):
        pass

class Wandering(State):
    """Wander from point to point on the screen"""
    def __init__(self, npc):
        State.__init__(self, "wandering", npc)

    def doActions(self, group):
        self.npc.move()

    """If the point has been reached, begin waiting"""
    def checkConditions(self, group):
        if self.npc.rect.collidepoint(self.npc.destination):
            return "waiting"
        else return None

    def entryActions(self, group):
        self.moving = True
        self.randomDestination()

    def exitActions(sel, group):
        self.moving = False

class Waiting(State):
    """Wait for a random number of frames"""
    def __init__(self, npc):
        State.__init__(self, "waiting", npc)
        self.time = None

    def doActions(self, group):
        

class StateMachine:
    """Collection of States that transitions between them"""
    def __init__(self):
        self.states = {}
        self.activeState = None

    def addState(seld, state):
        seld.states[state.name] = state

    def setState(self, stateName):
        if self.activeState is not None:
            self.activeState.exitActions()
        self.activeState = self.states[stateName]
        self.activeState.entryActions()

    def think(self, spriteGroup):
        if self.activeState is None:
            return
        self.activeState.doActions(spriteGroup)
        newStateName = self.activeState.checkConditions()
        if newStateName is not None:
            self.setState(newStateName)

    
        
