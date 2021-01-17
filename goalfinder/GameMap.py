import numpy as np
from astar import astar_search, null_heuristic
import math
from datetime import datetime
import json
import os


class GameMap:
    def __init__(self, width, height):
        self.players = dict()
        self.gameHeight = height
        self.gameWidth = width
        self.map = []
        
        numberLevel = math.ceil(math.log(width*height) / math.log(4)) - 1
        for level in range(1, numberLevel, 1):
            subarray = [0] * 4**level
            self.map.append(subarray)
        print(self.map)
        '''
        total_area = width * height
        factor = math.floor(math.sqrt(total_area)/2)**2
        while factor > 4:
            print(factor)
            subarray = [0] * math.floor(total_area / factor)
            self.map.append(subarray)
            factor = math.floor(math.sqrt(factor)/2)
            factor = factor ** 2
        self.map.append([0] * math.floor(total_area / 4))
        '''
        #print(factor)
        #print(self.map)

    def get_goal(self, data):
        """
        This is the initializer of the recursive goalfinder algorithm. First the top left and bottom right corner are set
        as the borders of the analysis. A single position to pursue will be returned.
        :param state: Current state of the game
        :param game: Game on which the analysis is done on
        :param tactic: Play offensive (>0) or defensive (<=0)
        :return: A single position on the field
        """
        for player in data['players']:
            currentPlayer = data['players'][player]
            #print("Player:")
            #print(currentPlayer)
            if player in self.players:
                oldPlayer = self.players[player]
                #print(oldPlayer)
                
                xSteps = max(abs(int(oldPlayer['x']) - int(currentPlayer['x'])),1)
                xStart = 0
                if int(oldPlayer['x']) < int(currentPlayer['x']):
                    xStart = int(oldPlayer['x'])
                else:
                    xStart = int(currentPlayer['x'])
                
                ySteps = max(abs(int(oldPlayer['y']) - int(currentPlayer['y'])), 1)
                yStart = 0
                if int(oldPlayer['y']) < int(currentPlayer['y']):
                    yStart = int(oldPlayer['y'])
                else:
                    yStart = int(currentPlayer['y'])
                    
                for xo in range(xSteps):
                    for yo in range(ySteps):
                        self.mapPosition(xStart + xo, yStart + yo)
            else:
                self.mapPosition(int(currentPlayer['x']), int(currentPlayer['y']))
            self.players[player] = data['players'][player]
        print("EVAL:")
        g = self.getNewGoal(0, 0, 0, 0)
        print("Our new goal is " + str(g))
        
        return g

    def getNewGoal(self, index, level, nx, ny):
        if level < len(self.map):
            #print(self.map[level])
            #print(index)
            selectedLevel = self.map[level][index*4:index*4+4]
            print(selectedLevel)
            newIndex = selectedLevel.index(min(selectedLevel))
            print(newIndex)
            xpart = newIndex % 2
            ypart = math.floor(newIndex / 2)
            xtile = math.ceil(self.gameWidth / 2**(level + 1))
            ytile = math.ceil(self.gameHeight / 2**(level + 1))
            return self.getNewGoal((index + newIndex), level+1, nx + (xpart * xtile), ny + (ypart * ytile))
        
        #print("Index: {} Level: {} LenLevel: {}".format(str(index), str(level), str(4**level)))
        #blib = (index % (2**(level + 1)) * self.gameWidth // 2**(level + 1), math.floor(index / (2**(level + 1)) * self.gameHeight / 2**(level + 1)))
        #print("INNN: {}".format(str(blib)))
        return (ny, nx)


    def mapPosition(self, x, y):
        for index, level in enumerate(self.map):
            levelSize = (index + 1) * 2
            #print("mapPosition x:{x} y:{y} gameWidth:{gameWidth} gameHeight:{gameHeight} levelSize: {levelSize} ".format(x=x, y=y, gameWidth=self.gameWidth, gameHeight=self.gameHeight, levelSize=levelSize))
            xpart = math.floor(x / (self.gameWidth / levelSize))
            ypart = math.floor(y / (self.gameHeight / levelSize)) * levelSize
            #print("xP " + str(xpart) + " yP " + str(ypart))
            index = xpart + ypart
            #print(index)
            try:
                level[index] += 1
            except IndexError as exception:
                pass