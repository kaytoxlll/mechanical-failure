# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

self.type = "slum"
#self.type = "house"
#self.type = "sewer"

self.script = ["doors"]
#self.script = ["dialogue line 1",
#               "dialogue line 2"]


self.npcname = "Anna"
self.npcref = "girl"
self.npclines = ["Eeek! Rats in the western warehouse!",
                 "Will you kill them?"]

self.sign = "Item shop"

self.east = "template"
self.west = "template"
self.north = "template"
self.south = ""
self.up = "template"
self.down = "template"

self.grid = ["WWWWWWWD.WWWWWWW", # door
             "WH.............W", # house
             "W............h.W", # treasure chest
             "W............c.W", # coin 
             "W.......<..>...W", # ladder down, ladder up
             "W.......w.g....W", # wrench, gun
             "W............#.W", # sign
             "...............l", # lock
             "................",
             "W..............W",
             "WMMMMMMMSSSSSSSW", # moat, sludge
             "W........a.p.b.W", # ammo, potion, powerbar
             "W..CA...CP.....W", # ammo shop item, potion shop item
             "W........n.r.t.W", # npc, rat, thief
             "W...B.O.T......W", # barrel, box, toxic barrel
             "WWWWWWWWWWWWWWWW",]
