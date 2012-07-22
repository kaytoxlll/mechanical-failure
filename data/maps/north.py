# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.name = "north"
self.song = "industrial.mp3"
self.floor = "boards"

def script(self):
    if len(self.currentmap.mobs) == 0:
        for s in self.currentmap.moveableGroup:
            s.kill()
        return True
    else:
        return False
self.script = script

self.east = ""
self.west = ""
self.north = "northend"
self.south = "start"

self.grid = ["wwwwwwwD.wwwwwww",
             "w.......t......w",
             "w..............w",
             "w..........b...w", 
             "w...b..........w",
             "w..............w",
             "w..............w",
             "w.......b......w",
             "w..............w",
             "w..............w",
             "w..............w",
             "w.....b........w",
             "w..............w",
             "w........b.....w",
             "w..............w",
             "wwwwwww..wwwwwww",]
