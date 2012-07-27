# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

Mechanical Failure - Readme

Sections:
	System Requirements
	Software Requirements
	Installation Instructions (Windows)
	Installation Instructions (Linux)
	Controlls
	Gameplay - Exploration
	Gameplay - Combat

System Requirements:
	PC and Linux (Mac in theory, untested)
	Just about any processor
	Just about any graphic card
	Keyboard and mouse

Software Requirements:
	Python 2, 32-bit version--------http://www.python.org/download/
	PyGame:-------------------------http://www.pygame.org/download.shtml

Installation Instructions (Windows):
	Step 1: Install Python 32-bit version 2.7:
	    Direct link to installer for Windows: http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi
	    To test if it installed properly:
	        Click on Start button from desktop
	        Search: python
	        Should see: Python (command line) as an option
	        It should open a command prompt
	Step 2: Install PyGame:
	    Direct link to installer for Windows: http://pygame.org/ftp/pygame-1.9.1.win32-py2.7.msi
	    To test that it installed properly:
	        Run Python (see step 1)
	        Type: import pygame (and click enter)
	        If nothing happens except another prompt line appears, then Pygame is installed
	Step 3: Run Mechanical Failure
	    Download the latest release of Mechanical Failure from http://code.google.com/p/mechanical-failure/downloads/list
	    Unzip the archive (right-click and select Extract)
	    Navigate to the newly unzipped folder
	    Double-click on the file: main.py

Installation Instructions(Linux):
	If you are using Linux, you can probably figure all this out :)

To Run the Game:
	Windows---------Double-click on main.py 
        Linux-----------Navigate the working directory to the folder with main.py in it
			Execute from the command line: python main.py

Controlls:
	W---------------Move up
	A---------------Move left
	S---------------Move down
	D---------------Move right
	SPACE-----------Drink a potion
	E---------------Examine / Talk
	L-CLICK---------Swing weapon
	R-CLICK---------Shoot gun (aim with mouse)
	Q---------------Place a bomb
	ESC-------------Quit

Gameplay - Exploration:
	Use the WASD keys to move the character.  The WASD keys act as arrow keys. 
For example: W is up, A is left, etc.  By holding two keys, you can move
diagonally.  
	To interact with various people and objects in the world, press E
while facing the target.  This is a good way to learn about something new.
	Some doors can only be unlocked when all the enemies in the area have 
been killed.  Some doors can only be unlocked by keys.  If you have one or more
keys in your inventory, press E to unlock a door.  This consumes one of your 
keys.
	If you see an item lying on the ground, walk over it to pick it up.
The HUD (heads-up-display) on the left side of the screen shows you what items 
you have.  If you see an item on display in a shop, examine it with E.

Gameplay - Combat:
	If an enemy attacks you, you will loose hit-points (HP).  If your HP 
reaches zero, you die: game over.  You can heal yourself by drinking potions 
(Spacebar) if you have any.
	Once you have a melee weapon, Left-click to swing it in the direction 
you are facing.  Enemies you hit will be injured and knocked back slightly.
For maximum effectiveness, hold Left-mouse-button to swing continuously. Melee
attacks can destroy some objects.
	Once you have a gun, Right-click to fire at a target.  The gun will 
fire wherever the mouse cursor is aimed.  If your target is moving, you may 
need to "lead" the target by aiming where they are going to be in order to 
hit them.
	Once you have bombs, press Q to place a bomb in front of you.  The bomb 
will blow up when it's fuse burns out, damaging anything nearby, including you! 
If a bomb is hit by an attack, it will blow up instantly.  Some walls can only
be destroyed by bombs.
