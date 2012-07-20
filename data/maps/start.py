# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.name = "start"
self.song = "industrial.mp3"
self.floor = "stone"

def script():
    dialogue("Talk to the woman to receive your quest")
self.script = script

self.npcname = "Anna"
self.npcref = "woman"
self.npclines = ["Eeek! Rats in the eastern warehouse!",
                 "Will you kill them?"]

self.east = "east"
self.west = ""
self.north = ""
self.south = ""

self.grid = ["wwwwwwwwwwwwwwww",
             "wh..........n..w",
             "w..............w",
             "w..............w", 
             "w..............w",
             "w..............w",
             "w..............w",
             "w...............",
             "w...............",
             "w..............w",
             "w..............w",
             "w...b..........w",
             "w..........b...w",
             "w......b.......w",
             "w..............w",
             "wwwwwwwwwwwwwwww",]
