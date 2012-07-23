# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.type = "slum"

def script(self):
    dialogue("Talk to the woman to receive your quest")
    return True
self.script = script

self.npcname = "Anna"
self.npcref = "woman"
self.npclines = ["Eeek! Rats in the western warehouse!",
                 "Will you kill them?"]

self.east = "east"
self.west = "west"
self.north = "north"
self.south = ""

self.grid = ["wwwwwww..wwwwwww",
             "wh..........n..w",
             "w..............w",
             "w............c.w", 
             "w...........cc.w",
             "w..............w",
             "w..............w",
             "...............l",
             "................",
             "w..............w",
             "w..............w",
             "w...b.......p..w",
             "w.....a....b...w",
             "w......b.......w",
             "w..............w",
             "wwwwwwwwwwwwwwww",]
