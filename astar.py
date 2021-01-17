import heapq
import math
""" Heuristics to be used for pathfinding algorithms """

def manhattan_distance(position, state, game):
    """ To be used with the a* algorithm ... """
    return abs(position[0]-game.goal[0]) + abs(position[1]-game.goal[1])


def manhattan_distance_position_dependend(position, goal):
    """ To be used for calculation purpose only """
    return abs(position[0]-goal[0]) + abs(position[1]-goal[1])


def null_heuristic(position, state, game):
    """ Always returns 0. Trivial heuristic. """
    return 0


def least_enemies_heuristic(position, state, game):
    """
    Heuristic that combines the missing manhattan distance from the current position to the goal with
    1 divided by the summed distance of the enemies. In theory:
    We want to take the path with the lowest probability to encounter an enemy, so we consider the distance to the goal
    (take the lowest) and we consider the distance to all enemies (take the highest --> so we take 1/that number)

    :param position: Considered position (not necessarily the current one)
    :param state: Current state (GameState obj. containing current position and info about enemies)
    :param game: Game obj.
    :return: heuristic value
    """
    result = manhattan_distance(position, state, game)
    summed_enemy_distance = 0
    # Enemy state: " ID : {'active': True, 'direction': 'down', 'x': 30, 'y': 33, 'speed': 1}
    for enemy in state.enemies:
        enemy_position = (state.enemies.get(enemy).get('y'), state.enemies.get(enemy).get('x'))
        summed_enemy_distance += manhattan_distance_position_dependend(position, enemy_position)
    # result += 1 / sum([manhattan_distance_position_dependend(position, (state.enemies.get(enemy).get('y'),
    # state.enemies.get(enemy).get('x'))) for enemy in state.enemies])
    try:
        return result + 1/summed_enemy_distance
    except ZeroDivisionError:
        return result

# To be continued ... Maybe develop some more heuristics for our special task


def astar_search(game, state, heuristics=null_heuristic):
    """
    A star algorithm.
    :param game: The game we are playing, keep in mind to have an updated field | Use Game datastructure
    :param state: Current Game State (especially current position) | Using GameState structure
    :param heuristics: heuristics to use with a* algorithm, default is the null heuristics
    :return:
    """
    minDist= math.inf
    minDistActions=['change_nothing']

    if game.is_goal_state(state.position):
        return 'reached'
    visited = []
    frontier = []
    heapq.heappush(frontier, (0, state.position, []))  # Costs, current position, action-history [left, right, ...]
    while frontier:
        prev_cost, node, actions = heapq._heappop_max(frontier)
        dist = game.getDistance(node)
        if dist < minDist:
            minDist = dist
            minDistActions = actions
        if game.is_goal_state(node):
            return actions
        if node not in visited:
            visited.append(node)
            for cost, successor, action in game.get_successor(node):
                if successor not in visited:
                    heapq.heappush(frontier, (prev_cost+cost+heuristics(node, state, game)-heuristics(successor, state, game), successor, actions+[action]))
    return minDistActions
