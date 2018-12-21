# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 01:51:27 2018

@author: gargk
"""
import random

class Minesweeper():
    def __init__(self,length:int, height:int, bombs:int) -> None:
        '''
        Create a Minesweeper object
        the dictionary's are created using helper methods self._generate_bombs and self._generate_clues
        self._revealed is empty at the start since no positions are selected
        self._revealed is updated in select and selectFirst

        '''
        self._length = length
        self._height = height
        self._revealed = {}
        self._bombpos = self._generate_bombs(bombs)
        self._clues = self._generate_clues()
        self._clues.update(self._bombpos)

    def _random_coordinate(self) -> (int,int):
        '''
        A helper method to create a random (x,y) with constraints as the length and height of the board tuple which
        used in self._generate_bombs
        '''
        return (random.randint(1,self._length) ,random.randint(1,self._height))


    def _generate_bombs(self,amount: int, bombs: dict = {}) -> {(int,int):'B'}:
        '''
        A helper method to generate a random amount of bombs, ensures each key is unique
        used to initially generate the bombs  in __init___
        used to generate 1 bomb in selectFirst if the user has selected a bomb as the first position
        '''
        bomb_dict = bombs.copy()
        for bomb in range(amount):
            random_coord = self._random_coordinate()
            while random_coord in bomb_dict.keys():
                random_coord = self._random_coordinate()
            bomb_dict[random_coord] = 'B'
        return bomb_dict


    def _generate_clues(self) -> {(int,int):int}:
        '''
        A helper method that initally generates clues to where the bombs are
        used in selectFirst method to generate clues when the bomb changes pos
        used in __init__ to create clues based on intial bomb positions
        '''
        clues_dict = {}
        for x in range(1,self._length + 1):
            for y in range(1,self._height + 1):
                if (x,y) not in self._bombpos:
                    clues_dict[(x,y)] = len(self._check_adj(x,y,self._bombpos))
        return clues_dict

    def _check_adj(self, x: int, y: int, finder: dict) -> {(int,int):'B' or int}:
        '''
        A helper method that creates a dictionary of the adjecent 8 values of a given position
        compares the adjecent values to another dictionary and creates a new dictionary containing the up to 8 values
        used in _open_0 to see if there are more 0's to open
        used in _generate_clues to see which positions are adjecent to bombs
        '''
        adj = {}
        for l in range(-1,2):
            for r in range(-1,2):
                if (x+l,y+r) in finder:
                    adj[(x+l, y+r)] = finder[(x+l,y+r)]
        return adj

    def _open_0(self,x: int,y: int) -> {(int,int):int}:
        '''
        a helper method that expands all 0's and returns a dictionary with the
        used in select
        used in selectFirst
        '''
        #checked initial value is the first set of adjecents
        checked = self._check_adj(x,y,self._clues)
        #since checking if the position is 0 is done in select method it is safe to assume first (x,y) pair is a zero
        zero = {(x,y):0}
        #this is used to keep track of values that are not 0
        numbers = {}
        #length of checked will equal zero when there are no zeros to check the adjecents of
        while len(checked) != 0:
            #keeps track of zeros in the current iteration
            zero_curr = {}
            for keys in checked:
                #check if key is 0 and not in the all zeros dict
                #this prevents repeating the same value
                if checked[keys] == 0 and keys not in zero:
                    #add in dict of all zeros
                    zero[keys] = self._clues[keys]
                    #add in dict of curr iteration of zeros
                    zero_curr[keys] = self._clues[keys]
                elif checked[keys] != 0:
                    #if its not zero add to numbers dict
                    numbers[keys] = self._clues[keys]
            #all values of checked are now in other dictionaries so reset checked
            checked = {}
            #iterate through the current zeros
            for keys in zero_curr:
                #keep updating the dictonary with the adjecents of all zero values
                checked.update(self._check_adj(keys[0],keys[1],self._clues))
        #combine the zeros and numbers dictionaries
        numbers.update(zero)
        return numbers

    def print(self) -> None:
        '''
        prints the current state of the board and what is revealed
        '''
        print(end = '   ')
        for w in range(1,self._length+1):
            if w < 10:
                print(w, end = "   ")
            else:
                print(str(w).format('>'), end = "  ")
        print("")
        for y in range(1,self._height+1):
            if(y < 10):
                print(y, end = '  ')
            else:
                print(y, end = ' ')
            for x in range(1,self._length+1):
                if (x,y) in self._revealed.keys():
                    print(self._revealed[(x,y)], end = '   ')
                else:
                    print('-', end = '   ')
            print('\n')


    def checkValid(self, x: int, y: int) -> bool:
        '''
        returns wether the point is a in the board constraints and revealed
        '''
        return 1 <= x <= self._length and 1 <= y <= self._height and (x,y) not in self._revealed


    def select(self, x: int, y: int) -> None:
        '''
        select a position and reveal the position and if zero reveal all neighbors
        '''
        if self._clues[(x,y)] == 0:
            self._revealed.update(self._open_0(x,y))
        else:
            self._revealed[(x,y)] = self._clues[(x,y)]


    def selectFirst(self, x: int, y: int) -> None:
        '''
        select a position and reveal the position and if zero reveal all neighbors
        if the position is a bomb remap the position of the bomb
        '''
        if (x,y) in self._bombpos.keys():
            self._bombpos = self._generate_bombs(1, self._bombpos)
            del self._bombpos[(x,y)]
        self._clues = self._generate_clues()
        self._clues.update(self._bombpos)
        if self._clues[(x,y)] == 0:
            self._revealed.update(self._open_0(x,y))
        self._revealed[(x,y)] = self._clues[(x,y)]


    def checkStatus(self) -> str:
        '''
        returns strings that tell the user the game status based of game win or loss conditions
        '''
        if 'B' in self._revealed.values():
            self._revealed.update(self._bombpos)
            return 'Bomb hit! You Loose \n'
        elif len(self._clues) - len(self._bombpos) == len(self._revealed) - list(self._revealed.values()).count('F'):
            return 'You Win \n'
        else:
            return 'Game in progress'


    def flag(self, x: int, y: int) -> None:
        '''
        adds the flag to the revealed to be printed
        '''
        self._revealed[(x,y)]  = 'F'


    def unflag(self, x: int, y: int) -> None or str:
        '''
        checks if position is unflagable and unflags otherwise returns an error string
        '''
        if (x,y) in self._revealed and self._revealed[(x,y)]  == 'F'and 1 <= x <= self._length and 1 <= y <= self._height:
            del self._revealed[(x,y)]
        else:
            return 'Cannot unflag \n'


    def _getSolution(self) -> None:
        '''
        prints the solution using the self._clues dictionary
        '''
        print(end = '   ')
        for w in range(1,self._length+1):
            if w < 10:
                print(w, end = "   ")
            else:
                print(str(w).format('>'), end = "  ")
        print("")
        for y in range(1,self._height+1):
            if(y < 10):
                print(y, end = '  ')
            else:
                print(y, end = ' ')
            for x in range(1,self._length+1):
                if (x,y) in self._clues.keys():
                    print(self._clues[(x,y)], end = '   ')
            print('\n')
