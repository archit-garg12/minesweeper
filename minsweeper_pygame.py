# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 16:37:54 2018

@author: gargk
"""

from minesweeper import Minesweeper

import pygame
class Board():
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.minesweeper = Minesweeper(self.settings.board_width, self.settings.board_height, self.settings.bombs)
    def update(self):
        for r in range(self.settings.board_width):
            for c in range(self.settings.board_height):
                rect = (((self.settings.margin + self.settings.square)*r + self.settings.margin),
                                                              ((self.settings.margin + self.settings.square)*c + self.settings.margin),
                                                              self.settings.square, self.settings.square)
                try:
                    number = self.minesweeper._revealed[(r+1,c+1)]
                    if number == 0:
                        pygame.draw.rect(self.screen, (211,211,211), rect)
                    elif number == 'F':
                        pygame.draw.rect(self.screen, (0,185,0), rect)
                    elif number == 'B':
                        pygame.draw.rect(self.screen, (185,0,0), rect)

                    for x in range(1,9):
                        if number == x:
                            image = pygame.image.load(str(x) + '.png')
                            self.screen.blit(image, rect)
                except:
                    pygame.draw.rect(self.screen, (255,255,255), rect)
    def game_over(self):
        if self.minesweeper.checkStatus() == 'Bomb hit! You Loose \n'  :
            pygame.time.wait(1000)
            return False
        elif self.minesweeper.checkStatus() == 'You Win \n':
            pygame.time.wait(1000)
            self.minesweeper = Minesweeper(self.settings.board_width, self.settings.board_height, self.settings.bombs)
            return True
        else:
            return True
