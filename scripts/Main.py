
from pymjin2 import *

MAIN_LCD_NAME        = "lcd"
MAIN_SEQUENCE_FINISH = "sequence.default.finish"
MAIN_SEQUENCE_START  = "sequence.default.start"
MAIN_SOUND_START     = "soundBuffer.default.start"
MAIN_TILE_MOVE_UP    = "move.default.liftTile"
MAIN_TILE_MOVE_DOWN  = "move.default.lowerTile"

class MainImpl(object):
    def __init__(self, c):
        self.c = c
        self.isStarted = False
        self.selectionsNb = None
    def __del__(self):
        self.c = None
    def displaySelectionsNb(self):
        self.c.set("lcd.$SCENE.$LCD.value", str(self.selectionsNb))
    def onSpace(self, key, value):
        print "Space pressed"
        if (self.isStarted):
            print "The game has already been started"
            return
        self.isStarted = True
        self.selectionsNb = 0
        self.displaySelectionsNb()
        self.c.setConst("SEQ", MAIN_SEQUENCE_START)
        self.c.set("$SEQ.active", "1")
    def setAssignFilterTileToDestination(self, key, value):
        tileName = self.c.get("filter.lastUsedTile")[0]
        self.c.set("filter.removeUsedTile", "1")
        self.c.set("destination.acceptTile", tileName)
        self.c.report("main.assignFilterTileToDestination", "0")
    def setAssignSelectedDestinationTileToFilter(self, key, value):
        tileName = self.c.get("destination.lastSelectedTile")[0]
        self.c.set("destination.removeSelectedTile", "1")
        self.c.set("filter.acceptTile", tileName)
        self.c.report("main.assignSelectedDestinationTileToFilter", "0")
    def setAssignSelectedSourceTileToFilter(self, key, value):
        tileName = self.c.get("source.lastSelectedTile")[0]
        self.c.set("source.removeSelectedTile", "1")
        self.c.set("filter.acceptTile", tileName)
        self.c.report("main.assignSelectedSourceTileToFilter", "0")
    def setClearLCD(self, key, value):
        self.c.set("lcd.$SCENE.$LCD.value", "")
        self.c.report("main.clearLCD", "0")
    def setDisplayResults(self, key, value):
        dst = self.c.get("destination.result")[0]
        src = self.c.get("source.result")[0]
        val = int(dst) - int(src)
        self.c.set("lcd.$SCENE.$LCD.value", str(val))
        self.c.report("main.displayResults", "0")
    def setFinishTheGameIfDestinationIsFull(self, key, value):
        dstFull = self.c.get("destionation.isFull")[0]
        if (dstFull == "1"):
            self.c.setConst("SEQ", MAIN_SEQUENCE_FINISH)
            self.c.set("$SEQ.active", "1")
        self.c.report("main.finishTheGameIfDestinationIsFull", "0")
    def setIncreaseSelectionsNbAndDisplayIt(self, key, value):
        self.selectionsNb = self.selectionsNb + 1
        self.displaySelectionsNb()
        self.c.report("main.increaseSelectionsNbAndDisplayIt", "0")
    # replayStartSound.
    def setReplayStartSound(self, key, value):
        self.c.setConst("SNDSTART", MAIN_SOUND_START)
        self.c.set("$SNDSTART.state", "play")
        # We don't wait for its completion for simplicity.
        self.c.report("main.replayStartSound", "0")

class Main(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Main")
        self.impl = MainImpl(self.c)
        self.c.setConst("SCENE",    sceneName)
        self.c.setConst("LCD",      MAIN_LCD_NAME)
        self.c.listen("input.SPACE.key", "1", self.impl.onSpace)

        self.c.provide("main.assignFilterTileToDestination",
                       self.impl.setAssignFilterTileToDestination)
        self.c.provide("main.assignSelectedDestinationTileToFilter",
                       self.impl.setAssignSelectedDestinationTileToFilter)
        self.c.provide("main.assignSelectedSourceTileToFilter",
                       self.impl.setAssignSelectedSourceTileToFilter)
        self.c.provide("main.clearLCD",         self.impl.setClearLCD)
        self.c.provide("main.displayResults",   self.impl.setDisplayResults)
        self.c.provide("main.finishTheGameIfDestinationIsFull",
                       self.impl.setFinishTheGameIfDestinationIsFull)
        self.c.provide("main.increaseSelectionsNbAndDisplayIt",
                       self.impl.setIncreaseSelectionsNbAndDisplayIt)
        self.c.provide("main.replayStartSound", self.impl.setReplayStartSound)

    def __del__(self):
        # Tear down.
        self.c.clear()
        # Destroy.
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Main(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance

