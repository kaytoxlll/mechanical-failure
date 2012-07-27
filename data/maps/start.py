# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.type = "slum"
#self.type = "house"
#self.type = "sewer"

#self.script = ["doors"]
self.script = [globalvars.hero.name + ": Ohhh... my head...",
               "Someone hit me from behind and stole my wallet!",
               "I remember... the thief was dressed in black...",
               "...and I think he ran east into the city...",
               "(Use WASD to move and E to examine/read/talk)"]

#self.npcname = ""
#self.npcref = ""
#self.npclines = [""]

self.sign = "City of Anarium (Glavos District) -->"

self.east = "start2"
self.west = ""
self.north = ""
self.south = ""
self.up = ""
self.down = ""

self.grid = ["WWWWWWWWWWWWWWWW",
             "WGGGGGGGGGGGGGGG",
             "WGGO..GGGGGGGGGG",
             "WGG.O.GGGGGGGGGG",
             "WGGGGGGGGGGGGGGG",
             "MMMMMMMGGGGGGGGG",
             "~~~~~~~......#..",
             "~~~~~~~.........",
             "~~~~~~~.........",
             "~...............",
             "~GGGGGGGGGGGGGGG",
             "~GGGGGGGGGGGGGGG",
             "~GGGGGGGGGGGGGGG",
             "~GGGGGGGGGGGGGGG",
             "~MMMMMMMMMMMMMMM",
             "~~~~~~~~~~~~~~~~"]
