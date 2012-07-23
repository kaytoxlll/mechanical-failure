# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.type = "slum"

def script(self):
    if len(self.currentmap.mobs) == 0:
        for s in self.currentmap.moveableGroup:
            s.kill()
        return True
    else:
        return False
self.script = script

self.east = "start"
self.west = "westend"
self.north = ""
self.south = ""
self.down = "down"

self.grid = ["wwwwwwwwwwwwwwww",
             "w......h.......w",
             "w..m...........w",
             "w..............w", 
             "w..............w",
             "w..............w",
             "w..............w",
             "d...............",
             "....r...........",
             "w..............w",
             "w..............w",
             "w.........b....w",
             "w..b...........w",
             "w........b.....w",
             "w..............w",
             "wwwwwwwwwwwwwwww",]
