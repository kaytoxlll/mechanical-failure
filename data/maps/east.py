# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.name = "east"
self.song = "industrial.mp3"
self.floor = "boards"

def script(self):
    return True
self.script = script

self.npcname = "Beth"
self.npcref = "woman"
self.npclines = ["Buy something, will ya!"]

self.east = ""
self.west = "start"
self.north = ""
self.south = ""

self.grid = ["wwwwwwwwwwwwwwww",
             "w..............w",
             "w......n.......w",
             "w..............w", 
             "w..A.A.A.A.A...w",
             "w..............w",
             "w............P.w",
             "...............w",
             ".............P.w",
             "w..............w",
             "w............P.w",
             "w..............w",
             "w............P.w",
             "w..............w",
             "w..............w",
             "wwwwwwwwwwwwwwww",]
