# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.name = "northend"
self.song = "industrial.mp3"
self.floor = "boards"

def script(self):
    dialogue("The theif is dead, yay")
    return True
self.script = script

self.east = ""
self.west = ""
self.north = ""
self.south = "north"

self.grid = ["wwwwwwwwwwwwwwww",
             "w..............w",
             "w..............w",
             "w.b....b...b...w", 
             "w..............w",
             "w.b....b...b...w",
             "w.cccc.........w",
             "w.cccc.........w",
             "w.cccc.........w",
             "w.cccc.........w",
             "w..............w",
             "w.b....b...b...w",
             "w..............w",
             "w.b....b...b...w",
             "w..............w",
             "wwwwwww..wwwwwww",]
