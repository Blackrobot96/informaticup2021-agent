from game_state import GameState
from game import Game
import numpy as np

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