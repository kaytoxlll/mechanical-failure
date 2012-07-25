# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.type = "slum"
#self.type = "house"
#self.type = "sewer"

#self.script = ["doors"]
#self.script = [""]

self.npcname = "Sharon"
self.npcref = "woman"
self.npclines = ["Thinking of entering the sewer?",
                 "Well, I don't recommend it, rats are vicious",
                 "Don't even think about it if you don't have a weapon!"]

self.sign = "Sewer west entrance (Danger! Rats!!)"

self.east = ""
self.west = "glavosN"
self.north = ""
self.south = "glavosE"
self.up = ""
self.down = "sewerW1"

self.grid = ["WWWWWWWWWWWWWWWW",
             "W......M.#.....W",
             "W.O....M.....<.W",
             "W..O...M.......W",
             "W......M...MMMMW",
             "W..............W",
             "W..............W",
             "...............W",
             "...............W",
             "W..............W",
             "WH.............W",
             "W..............W",
             "W...........n..W",
             "W..............W",
             "W..............W",
             "WWWWWWW..WWWWWWW",]
