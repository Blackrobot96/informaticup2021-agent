import numpy as np
import math

# w x-> 0 0
# 0 0 0
# 0 0 y z->


# Split the game_field and return a bunch of tuples for the coordinates of the squares
# Scale determines the size of the field
# return: Returns a list of fields with top left corner and bottom right corner coordinates and a given value
class LastGoalfinder:
    def __init__(self, game, scale):
        self.fields = []
        self.scale = scale
        self.width = game.field_width
        self.height = game.field_height
        self.players = dict()
        tl_corner = [0, 0]
        br_corner = [scale, scale]
        while br_corner[0] < self.height:
            while br_corner[1] < self.width:
                self.fields.append([[tl_corner, br_corner], 0])
                tl_corner[1] += scale
                br_corner[1] += scale
                if br_corner[1] + scale >= self.width:  # Extend the size of the last field to reach the border
                    br_corner[1] = self.width
            tl_corner[1] = 0
            br_corner[1] = 0
            tl_corner[0] += scale
            br_corner[0] += scale
            if br_corner[0] + scale >= self.height:
                br_corner[0] = self.height


    # Increment at the appropriate location
    def increment(self, x, y):
        y_scale = math.floor(self.width / self.scale)
        x_scale = math.floor(self.height / self.scale)
        y_index = math.floor(y/y_scale) + y % y_scale
        x_index = x % x_scale
        index = x_index * y_index + y_index
        print(index)
        self.fields[index][1] += 1

    # Choose a random position in the field
    def choose_rand_pos(self, tl_corner, br_corner):
        return tuple([np.random.randint(tl_corner[0], br_corner[0]), np.random.randint(tl_corner[1], br_corner[1])])

    def getGoalFromFields(self):
        temp = -1
        choice = self.fields[0]
        for field in self.fields:
            if field[1] > temp:
                temp = field[1]
                choice = field[1]
        return choose_rand_pos(choice[0][0], choice[0][1])


    # Choose the field with the highest value and return the corner coordinates
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
            # print("Player:")
            # print(currentPlayer)
            if player in self.players:
                oldPlayer = self.players[player]
                # print(oldPlayer)

                xSteps = max(abs(int(oldPlayer['x']) - int(currentPlayer['x'])), 1)
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
                        self.increment(xStart + xo, yStart + yo)
            else:
                self.increment(int(currentPlayer['x']), int(currentPlayer['y']))
            self.players[player] = data['players'][player]
        g = self.getGoalFromFields()
        print(g)
        return g
