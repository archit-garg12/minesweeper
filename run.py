# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 21:05:45 2018

@author: gargk
"""

import pygame
from minsweeper_pygame import Board
from settings import Settings
def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode([settings.screen_width, settings.screen_height])
    mine = Board(settings, screen)
    turn_num = 0
    while mine.game_over():
        turn_num = check_events(mine, turn_num)
        mine.update()
        pygame.display.flip()
    pygame.quit()
def check_events(board, turn):
    '''
    Checks for key events and quits if the x is pressed
    '''
    for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click(event, board, turn)
                turn += 1
                return turn
            if event.type == pygame.QUIT:
                pygame.quit()
    return turn
def mouse_click(event, board, turn):
    mousepos = pygame.mouse.get_pos()
    col = mousepos[0] // (board.settings.square + board.settings.margin) +1
    row = mousepos[1] // (board.settings.square + board.settings.margin) +1
    if event.button == 1 and board.minesweeper.checkValid(col,row):
        print('colmouse',mousepos[1],'rowmouse', mousepos[0])
        print('col',col,'row', row)
        if turn == 0:
            board.minesweeper.selectFirst(col, row)
        else:
            board.minesweeper.select(col, row)
        board.minesweeper.checkStatus()
    if event.button == 3 and turn != 0 and board.minesweeper.checkValid(col,row):
        board.minesweeper.flag(col, row)
    elif event.button == 3:
        board.minesweeper.unflag(col, row)

run_game()
