import asyncio
import json
import websockets
from datetime import datetime
import numpy as np
import sys
from util_functions import init_game, get_curr_state
import heapq
from game_state import GameState
import os
from astar import astar_search, manhattan_distance, least_enemies_heuristic
from goalfinder import recursive_goalfinder
from goalfinder import GameMap

"""
Execute this file to run agent
"""

np.set_printoptions(threshold=sys.maxsize)


def update_game_state(game, game_state, action, agent_index):
    """
    Function to update the game state structure.

    :param game: Game Structure
    :param game_state: prior game State
    :param action: action to be performed
    :param agent_index: index of agent [difference between our and other agent]
    :return: new state with updated position and updated "alive" status
    """
    directions = {'left': (0, -1), 'up': (-1, 0), 'right': (0, 1), 'down': (1, 0)}
    if str(agent_index) == str(game.our_agent_id):
        new_position = (game_state.position[0]+directions[str(action)][0], game_state.position[1]+directions[str(action)][1])
        alive = True
        if not game.within_bounds(new_position) or game.field[new_position[0], new_position[1]] != 0:
            print(new_position, game.field[new_position])
            alive = False
        res = GameState(new_position, game_state.direction, alive, game_state.speed)
        res.enemies = dict(game_state.enemies)
        # print(res)
        return res
    else:
        new_position = (game_state.enemies[str(agent_index)].get('y')+directions[str(action)][0], game_state.enemies[str(agent_index)].get('x')+directions[str(action)][1])
        alive = True
        if not game.within_bounds(new_position) or game.field[new_position[0], new_position[1]] != 0:
            alive = False
        res = GameState(game_state.position, game_state.direction, True, game_state.speed)
        res.enemies = dict(game_state.enemies)
        res.enemies[str(agent_index)]['y'], res.enemies[str(agent_index)]['x'] = new_position
        res.enemies['active'] = alive
        return res


def alpha_beta(game, game_state, enemies_in_view):
    """
    Function to plan and call alpha-bate pruning algorithm
    :param game: The Game object
    :param game_state: The current GameState
    :return: the action yield by the alpha-beta algorithm
    """
    res = []
    a = -float('inf')
    b = float('inf')
    action_counter = []
    depth = 10  # Set dynamically!
    alpha_beta_pruning(game, game_state, depth, True, game.our_agent_id, a, b, action_counter, enemies_in_view)

    # Sort action by value
    for value, action in action_counter:
        heapq.heappush(res, (-value, action))

    # debug only!
    try:
        result = heapq.heappop(res)
    except IndexError:
        result = (0, 'change_nothing')

    print(result)

    return result


def alpha_beta_pruning(game, game_state, depth, maximizing_player, agent_index, a, b, action_counter, enemies_in_view):
    """
    Function to actually perform the alpha beta algorithm.

    :param game: Game object containing especially the field and has to be manipulable
    :param game_state: current state of the game (GameState) object
    :param depth: maximum recursion depth of the algorithm
    :param maximizing_player: boolean to say whether it's our turn
    :param agent_index: the current agent's turn [the ID of the agent]
    :param a: alpha-bound
    :param b: beta-bound
    :param action_counter: initially empty list that will be yield
    :param enemies_in_view: A list of all enemy indices which are in range
    :return: an unordered list containing each possible action and its value based on its estimated utility
    """
    if agent_index > len(enemies_in_view)+1:
        agent_index = 1
    if depth == 0 or game_state.is_win(enemies_in_view) or not game_state.alive:
        # Write evaluation function pls
        return game.evaluate_field(game_state, enemies_in_view)
    if maximizing_player:
        value = -float('inf')
        # put get legal actions ...
        for action in game.get_legal_actions(game_state, agent_index):
            action = action[2]
            successor = game.generate_successor(game_state, game.our_agent_id, action)
            # "game" instead of successor???????
            next_state = update_game_state(game, game_state, action, agent_index)
            value = max(value, alpha_beta_pruning(successor, next_state, depth, False, 2, a, b, [], enemies_in_view))
            a = max(a, value)
            action_counter.append((value, action))
            if a > b:
                break
        return value
    elif len(enemies_in_view) > 1:
        value = float("inf")
        for action in game.get_legal_actions(game_state, agent_index):
            action = action[2]
            successor = game.generate_successor(game_state, agent_index, action)
            next_state = update_game_state(game, game_state, action, agent_index)
            value = min(value, alpha_beta_pruning(successor, next_state, depth - 1, True, agent_index + 1, a, b, [], enemies_in_view)) if agent_index == game_state.getNumAgents() - 1 else min(value, alpha_beta_pruning(successor, game_state, depth, False, agent_index + 1, a, b, [], enemies_in_view))
            b = min(b, value)
            action_counter.append((value, action))
            if b < a:
                break
        return value
    else:
        value = float("inf")
        for action in game.get_legal_actions(game_state, agent_index):
            action = action[2]
            successor = game.generate_successor(game_state, agent_index, action)
            next_state = update_game_state(successor, game_state, action, agent_index)
            value = min(value, alpha_beta_pruning(successor, next_state, depth - 1, True, 1, a, b, [], enemies_in_view))
            b = min(b, value)
            action_counter.append((value, action))
            if b < a:
                break
        return value

# Test area
def alpha_beta_test(game, game_state, enemies_in_view):
    """
    Function to plan and call alpha-bate pruning algorithm
    :param game: The Game object
    :param game_state: The current GameState
    :return: the action yield by the alpha-beta algorithm
    """
    res = []
    a = -float('inf')
    b = float('inf')
    action_counter = []
    depth = 3  # Set dynamically!
    enemies_in_view = [str(game.our_agent_id)]+enemies_in_view
    alpha_beta_pruning_test(game, game_state, depth, a, b, action_counter, enemies_in_view)

    print(action_counter)

    # Sort action by value
    for value, action in action_counter:
        heapq.heappush(res, (-value, action))

    # debug only!
    try:
        result = heapq.heappop(res)
    except IndexError:
        result = (0, 'change_nothing')

    print("AB-RESULT: ", result)

    return result

def alpha_beta_pruning_test(game, game_state, depth, a, b, action_counter, enemies_in_view):
    """
    Function to actually perform the alpha beta algorithm.

    :param game: Game object containing especially the field and has to be manipulable
    :param game_state: current state of the game (GameState) object
    :param depth: maximum recursion depth of the algorithm
    :param a: alpha-bound
    :param b: beta-bound
    :param action_counter: initially empty list that will be yield
    :param enemies_in_view: A list of all enemy indices which are in range
    :return: an unordered list containing each possible action and its value based on its estimated utility
    """
    # Idea: treat enemies_in_view as endless queue
    # print(game_state)
    #print(enemies_in_view)
    player = enemies_in_view.pop(0)
    enemies_in_view.append(player)
    if str(player) == str(game.our_agent_id):
        maximizing_player = True
    else:
        maximizing_player = False
    if depth == 0 or game_state.is_win([enemy for enemy in enemies_in_view if str(enemy) != str(game.our_agent_id)]) or not game_state.alive:
        # Write evaluation function pls
        return game.evaluate_field(game_state, [enemy for enemy in enemies_in_view if str(enemy) != str(game.our_agent_id)])
    if maximizing_player:
        value = -float('inf')
        # put get legal actions ...
        for action in game.get_legal_actions(game_state, player):
            action = action[2]
            try:
                successor = game.generate_successor(game_state, game.our_agent_id, action)
            except Exception:
                continue
            next_state = update_game_state(game, game_state, action, game.our_agent_id)
            value = max(value, alpha_beta_pruning_test(successor, next_state, depth-1, a, b, [], enemies_in_view[:]))
            a = max(a, value)
            action_counter.append((value, action))
            if a > b:
                break
        return value
    else:
        value = float("inf")
        for action in game.get_legal_actions(game_state, player):
            action = action[2]
            try:
                successor = game.generate_successor(game_state, player, action)
            except Exception:
                continue # Since this action kills us, we stop evaluating this path!
            next_state = update_game_state(game, game_state, action, player)
            value = min(value, alpha_beta_pruning_test(successor, next_state, depth, a, b, [], enemies_in_view[:]))
            b = min(b, value)
            action_counter.append((value, action))
            if b < a:
                break
        return value


states = []

def correct_bounds(game, positions):
    # Careful! field_height works only if we have y coordinates or the field has equal size!!
    result = list(positions[0]) + list(positions[1])
    if positions[0][0] < 0:
        result[0] = 0
    if positions[0][1] >= game.field_height:
        result[1] = game.field_height-1
    if positions[1][0] < 0:
        result[2] = 0
    if positions[1][1] >= game.field_height:
        result[3] = game.field_width
    return ((result[0], result[1]), (result[2], result[3]))


async def play():
    """ Limited Alpha Beta Agent """
    async with websockets.connect("ws://localhost:8081") as websocket:
        print("Waiting for initial state...", flush=True)
        flag = 'ToDo'
        game = None
        current_state = None
        gameMap = None
        while True:
            state_json = await websocket.recv()
            data = json.loads(state_json)
            
            if flag == 'ToDo':
                game = init_game(data)

            if gameMap is None:
                print("ASADASD")
                gameMap = GameMap.GameMap(game.field_width, game.field_height)

            # update game and states
            game.update_field(data.get('cells'))
            current_state = get_curr_state(game, data)

            # Area to consider to check whether to perform alpha-beta
            agent_view = ((current_state.position[0] - 3, current_state.position[0] + 4), (current_state.position[1] - 3, current_state.position[1] + 4))
            agent_view = correct_bounds(game, agent_view)
            enemies_in_view = current_state.get_enemy_within_bounds(agent_view[0], agent_view[1])
            # DEBUG: # print(game.field[agent_view[0][0]:agent_view[0][1], agent_view[1][0]:agent_view[1][1]])
            # DEBUG: # print(enemies_in_view)

            # Condition to perform alpha-beta: Here: At least one enemy is within a 7x7 grid around our agent
            '''if enemies_in_view:
                action = alpha_beta_test(game, current_state, enemies_in_view)

                action = game.get_action_from_policy(current_state, [action[1]])
            else:
                # Act on some different manner (use another agent)
                # For debugging reasons it's set to alpha beta algorithm
                # action = alpha_beta_test(game, current_state, enemies_in_view)
                if game.goal is None:
                    #game.goal = recursive_goalfinder.get_goal(game, current_state, -1)
            '''

            game.goal = gameMap.get_goal(data)
            policy = astar_search(game, current_state)
            action = game.get_action_from_policy(current_state, policy)

            data["yourgoal"] = game.goal
            #action = astar_search(game, current_state, manhattan_distance)
            #print(action)
            #action = game.get_action_from_policy(current_state, action)

            # Send action to the server
            action_json = json.dumps({"action": action})
            states.append(data)
            await websocket.send(action_json)



if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(play())
    finally:
        now = datetime.now()
        # Here comes stuff for later GUI-View
        # f = open("."  + "/" + now.strftime("%Y-%m-%dT%H-%M-%S") + ".json", "w")
        f = open("." + "/" + now.strftime("%Y-%m-%dT%H-%M-%S") + str(np.random.randint(1, 9999)) + ".json", "w")
        f.write(json.dumps({"game": states}))
        f.close()

