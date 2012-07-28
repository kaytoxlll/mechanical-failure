# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.type = "slum"
#self.type = "house"
#self.type = "sewer"

#self.script = ["doors"]
self.script = [globalvars.hero.name + ": Now where did that thief go...",
               "Better ask around town!"]

self.npcname = "Anna"
self.npcref = "woman"
self.npclines = ["That no-good husband of mine!",
                 "If I had my wrench I'd wallop him good...",
                 "...but it's locked in my closet and I lost the key."]

#self.sign = ""

self.east = "glavosCenter"
self.west = "start2"
self.north = "glavosNW"
self.south = "glavosSW"
self.up = ""
self.down = ""

self.grid = ["WWWWWWW..WWWWWWW",
             "WH........BB...W",
             "W...........MM.W",
             "W...........~~.W",
             "W..............W",
             "W..............W",
             "W..............W",
             "................",
             "...........n....",
             "W..............W",
             "WH.............W",
             "W.........O....W",
             "W...........MM.W",
             "W...........~~.W",
             "W..............W",
             "WWWWWWW..WWWWWWW",]
