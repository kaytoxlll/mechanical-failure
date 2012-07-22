# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.name = "west"
self.song = "industrial.mp3"
self.floor = "boards"

def script():
    if len(self.currentmap.mobs) == 0:
        self.currentmap.moveableGroup.empty()
        return True
    else:
        return False
self.script = script

self.east = "start"
self.west = "westend"
self.north = ""
self.south = ""

self.grid = ["wwwwwwwwwwwwwwww",
             "w.......r...r..w",
             "w..............w",
             "w..........b...w", 
             "w...b..........w",
             "w..............w",
             "w..............w",
             "d.......b.......",
             "d...............",
             "w..............w",
             "w..............w",
             "w.....b........w",
             "w...........r..w",
             "w........b.....w",
             "w............r.w",
             "wwwwwwwwwwwwwwww",]
