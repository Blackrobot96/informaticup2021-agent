import asyncio
import json
import websockets
from datetime import datetime
import numpy as np
import sys
from game import Game
from game_state import GameState
from astar import astar_search, least_enemies_heuristic
from goalfinder import recursive_goalfinder as rgf

states = []


def init_game(data):
    """
    Function to initialize and return a game object given the json with game information from the server
    :param data:
    :return:
    """
    our_id = data['you']
    width = data['width']
    height = data['height']
    game = Game(np.array(data['cells']), width, height, our_id)
    return game


def get_curr_state(game, data):
    # Retrieve data of the agent
    agent_data = data['players'].get(str(data["you"]))
    # Use agent data to build up a current state
    current_state = GameState((agent_data.get('y'), agent_data.get('x')), agent_data.get('direction'),
                              agent_data.get('active'), agent_data.get('speed'))

    # Getting enemies data
    for player in data['players']:
        if int(player) == int(game.our_agent_id):
            continue
        current_state.enemies[player] = data['players'].get(str(player))

    return current_state


async def play():
    async with websockets.connect("ws://localhost:8081") as websocket:
        print("Waiting for initial state...", flush=True)
        np.set_printoptions(threshold=sys.maxsize)
        flag = 'ToDo'
        game = None
        while True:
            state_json = await websocket.recv()
            data = json.loads(state_json)
            states.append(data)  # Important for recreation of the game?
            # Initialize the Game just the very first time we receive the data from the server
            if flag == 'ToDo':
                game = init_game(data)
                flag = 'done'

            # Update data here
            game.update_field(data['cells'])
            current_state = get_curr_state(game, data)

            # Stop spamming stuff to the server once we are dead
            if not current_state.alive:
                print("You are dead ...")
                break
            if game and game.goal is None:
                # Goal to search, hardcoded for test purpose only.
                # Later we may set the goal dynamically using some Machine Learning to predict the best spot on the map
                game.goal = (10, 10)
                # game.goal = rgf.get_goal(game, current_state, -1)

            # Figure out policy for next step
            if game.goal is not None:
                if game.is_goal_state(current_state.position):
                    """ Set new goal ... """
                    game.goal = rgf.get_goal(game, current_state, -1)
                policy = astar_search(game, current_state, least_enemies_heuristic)
                if policy == 'reached':
                    raise Exception("Shouldn't be reached ...")
                action = game.get_action_from_policy(current_state, policy)

            # Send action to the server
            action_json = json.dumps({"action": action})
            await websocket.send(action_json)

# Now you can import this file and use the Game-structure
if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(play())
    finally:
        now = datetime.now()
        # Here comes stuff for later GUI-View
