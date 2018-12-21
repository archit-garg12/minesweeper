# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 18:11:52 2018

@author: gargk
"""

class Settings():
    def __init__(self):
        self.board_height = 60
        self.board_width = 60
        self.square = 15
        self.margin = 1
        self.screen_height = self.board_height * (self.square + self.margin) + self.margin
        self.screen_width = self.board_width * (self.square + self.margin) + self.margin
        self.bombs = 3599
