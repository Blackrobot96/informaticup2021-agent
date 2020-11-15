import numpy as np
import sys
import random
import heapq

"""
Environment to test some algorithms ... 
"""


class Game:
    def __init__(self, field, goal):
        self.field = field
        self.field_height = len(field)
        self.field_width = len(field[0])
        self.actions = ['left', 'right', 'up', 'down']
        self.actions_map = {'left': (0, -1), 'right': (0, 1), 'up': (-1, 0), 'down': (1, 0)}
        self.goal = goal
        self._MYPOSITION = 2
        self._OBSTACLE = [2, 3]

    def get_successor(self, position):
        neighbours = []
        if self.within_bounds((position[0] - 1, position[1])) and self.field[position[0] - 1, position[1]] not in self._OBSTACLE:
            neighbours.append((1, (position[0] - 1, position[1]), 'up'))
        if self.within_bounds((position[0], position[1] - 1)) and self.field[position[0], position[1] - 1] not in self._OBSTACLE:
            neighbours.append((1, (position[0], position[1] - 1), 'left'))
        if self.within_bounds((position[0], position[1] + 1)) and self.field[position[0], position[1] + 1] not in self._OBSTACLE:
            neighbours.append((1, (position[0], position[1] + 1), 'right'))
        if self.within_bounds((position[0] + 1, position[1])) and self.field[position[0] + 1, position[1]] not in self._OBSTACLE:
            neighbours.append((1, (position[0] + 1, position[1]), 'down'))
        return neighbours

    def is_goal_state(self, position):
        return position == self.goal

    def within_bounds(self, position):
        return 0 <= position[0] < self.field_height and 0 <= position[1] < self.field_width

    def next_position(self, position, action):
        position = list(position)
        if action == 'up':
            position[0] -= 1
        if action == 'left':
            position[1] -= 1
        if action == 'right':
            position[1] += 1
        if action == 'down':
            position[0] += 1
        return position

    def perform_actions(self, position, policy):
        """
        Performs all actions of a policy
        :param position: Starting position
        :param policy: Policy (strings of names of actions)
        :return:
        """
        for action in policy:
            self.field[position[0], position[1]] = self._MYPOSITION
            position = self.next_position(position, action)


    def __repr__(self):
        res = ""
        res += str(self.field) + "\n"
        res += "Field height: " + str(self.field_height) + "\n"
        res += "Field width: " + str(self.field_width) + "\n"
        return res


class GameState:
    def __init__(self, position):
        self.position = position

    def __str__(self):
        res = "Position: " + str(self.position)
        return res


def manhattan_distance(position, goal):
    return abs(position[0]-goal[0]) + abs(position[1]-goal[1])


def null_heuristic(position, goal):
    return 0


def astar_search(game, state, heuristics=null_heuristic):
    """
    A star algorithm.
    :param state: Current Game State (especially current position)
    :param goal: Goal position
    :param heuristics: heuristics to use with a* algorithm, default is the null heuristics
    :return:
    """
    visited = []
    frontier = []
    heapq.heappush(frontier, (0, state.position, []))  # Costs, current position, action-history [left, right, ...]
    while frontier:
        prev_cost, node, actions = heapq.heappop(frontier)
        if game.is_goal_state(node):
            return actions
        if node not in visited:
            visited.append(node)
            for cost, successor, action in game.get_successor(node):
                if successor not in visited:
                    heapq.heappush(frontier, (prev_cost+cost+heuristics(node, game.goal)-heuristics(successor, game.goal), successor, actions+[action]))


np.set_printoptions(threshold=sys.maxsize)
initial_pos = random.randint(0, 8), random.randint(0, 8)

game = Game(np.zeros((9, 9)), (0, 0))
game.field[0, 0] = 8

policy = astar_search(game, GameState((8, 0)))
print(policy)

if policy is not None:
    game.perform_actions((8, 0), policy)

game.field[initial_pos[0], initial_pos[1]] = 9

print(game)
