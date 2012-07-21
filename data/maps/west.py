# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.name = "west"
self.song = "industrial.mp3"
self.floor = "boards"

def script():
    dialoge("This is the item shop")
    return True
self.script = script

self.npcname = "Beth"
self.npcref = "woman"
self.npclines = ["Buy something!"]

self.east = "start"
self.west = ""
self.north = ""
self.south = ""

self.grid = ["wwwwwwwwwwwwwwww",
             "w..............w",
             "w......n.......w",
             "w..............w", 
             "w...AAA...PPP..w",
             "w..............w",
             "w..............w",
             "w...............",
             "w...............",
             "w..............w",
             "w..............w",
             "w..............w",
             "w..............w",
             "w..............w",
             "w..............w",
             "wwwwwwwwwwwwwwww",]
