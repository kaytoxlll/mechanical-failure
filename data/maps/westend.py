# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.type = "house"

def script(self):
    dialogue("Yay, rats dead, barrels safe")
    dialogue("have some coins")
    return True
self.script = script

self.east = "west"
self.west = ""
self.north = ""
self.south = ""

self.grid = ["wwwwwwwwwwwwwwww",
             "w..............w",
             "w..............w",
             "w.b....b...b...w", 
             "w..............w",
             "w.b....b...b...w",
             "w.cccc.........w",
             "w.cccc..........",
             "w.cccc..........",
             "w.cccc.........w",
             "w..............w",
             "w.b....b...b...w",
             "w..............w",
             "w.b....b...b...w",
             "w..............w",
             "wwwwwwwwwwwwwwww",]
