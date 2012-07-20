# Copyright (c) 2012 Bailey Mihajlich
# Licensed under the GNU GPL v.2
# See license.txt for licence information

"""Wrapper class for pgame music, has the added feature that
if a song is already playing, telling the music player to play
it will not cause it to restart.
"""

import pygame
from os.path import join

pygame.init()

class MusicPlayer():

    def __init__(self, song=None):
        self.song = join("data", "music", song)
        if song is not None:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(-1, 0.0)

    def play(self, song):
    """Start playing the song.
    If it is already playing, do not interrupt.
    """
    songfile = join("data", "music", song)
    if songfile <> self.song:
        self.song = songfile
        pygame.mixer.music.load(songfile)
        pygame.mixer.music.play(songfile)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def fadeout(time=1000):
        pygame.mixer.music.fadeout(time)
