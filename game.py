import numpy as np
from astar import manhattan_distance_position_dependend


class Game:
    """ Game class. Takes the field (numpy array, width, height and our agents id """
    def __init__(self, field, width, height, my_id):
        self.field = field
        self.field_height = height
        self.field_width = width
        self.actions = ['turn_left', 'turn_right', 'change_nothing']
        self.directions = ['left', 'right', 'up', 'down']
        self.goal = None
        self.our_agent_id = my_id

    def get_successor(self, position):
        """
        Method to get all possible successors from a position.
        Works for any agent since we just compare for field[][]=0
        :param position: position to get the successors from
        :return: a list of all possible successors formatted as -> (costs, position, action_performed)
        """
        neighbours = []
        # If you define all obstacles do ... self.field[...] not int self._OBSTACLES
        if self.within_bounds((position[0] - 1, position[1])) and self.field[position[0] - 1, position[1]] == 0:
            neighbours.append((1, (position[0] - 1, position[1]), 'up'))
        if self.within_bounds((position[0], position[1] - 1)) and self.field[position[0], position[1] - 1] == 0:
            neighbours.append((1, (position[0], position[1] - 1), 'left'))
        if self.within_bounds((position[0], position[1] + 1)) and self.field[position[0], position[1] + 1] == 0:
            neighbours.append((1, (position[0], position[1] + 1), 'right'))
        if self.within_bounds((position[0] + 1, position[1])) and self.field[position[0] + 1, position[1]] == 0:
            neighbours.append((1, (position[0] + 1, position[1]), 'down'))
        return neighbours

    def get_legal_actions(self, game_state, agent_id):
        """
        Method to get all legal actions for an agent. Method makes use of get_successor.

        :param game_state: Current game state.
        :param agent_id: ID of the agent to get the legal actions from
        :return: List of all legal actions formatted as in get_succesors
        """
        if str(agent_id) == str(self.our_agent_id):
            return self.get_successor(game_state.position)
        return self.get_successor((game_state.enemies[str(agent_id)]['y'], game_state.enemies[str(agent_id)]['x']))

    def generate_successor(self, game_state, agent_id, action):
        """
        Function to perform action. We assume the action passed in is valid.

        :param game_state: Current state of the game
        :param agent_id: Index ob agent to perform the action
        :param action: action to be performed. In this level it's just [up, left, down, right]
        :return: Return new Game object with this action performed
        """
        directions = {'left': (0, -1), 'up': (-1, 0), 'right': (0, 1), 'down': (1, 0)}
        field = np.array(self.field)
        if str(agent_id) == str(self.our_agent_id):
            field[game_state.position[0]+directions[str(action)][0], game_state.position[1]+directions[str(action)][1]] = self.our_agent_id
        else:
            field[game_state.enemies[str(agent_id)]['y'] + directions[str(action)][0], game_state.enemies[str(agent_id)]['x'] + directions[str(action)][1]] = agent_id
        return Game(field, self.field_width, self.field_height, self.our_agent_id)

    def is_goal_state(self, position):
        return position == self.goal

    def within_bounds(self, position):
        return 0 <= position[0] < self.field_height and 0 <= position[1] < self.field_width

    def get_action_from_policy(self, state, policy):
        """
        Function to come up with action considering state and policy

        :param state:
        :param policy:
        :return: action to perform
        """
        if not policy:
            return 'change_nothing'
        # Later: If more than n times consequently the same action in policy, increase in speed
        if state.direction == policy[0]:
            return 'change_nothing'
        if state.direction == 'up':
            if policy[0] == 'left':
                return 'turn_left'
            elif policy[0] == 'right':
                return 'turn_right'
        if state.direction == 'down':
            if policy[0] == 'left':
                return 'turn_right'
            elif policy[0] == 'right':
                return 'turn_left'
        if state.direction == 'left':
            if policy[0] == 'up':
                return 'turn_right'
            if policy[0] == 'down':
                return 'turn_left'
        if state.direction == 'right':
            if policy[0] == 'up':
                return 'turn_left'
            if policy[0] == 'down':
                return 'turn_right'
        # default ...
        return 'change_nothing'

    def get_valid_random_position(self):
        """ Yet no valid position, just totally random """
        return tuple([np.random.randint(0, self.field_height), np.random.randint(0, self.field_width)])

    def update_field(self, new_field):
        self.field = np.array(new_field)

    def evaluate_field(self, current_state, enemies_in_view):
        """
        Method to evaluate the field and return a "utility".

        :param current_state: Current State of the Game (GameState object)
        :param enemies_in_view: Data of all enemies to be considered
        :return:
        """
        """
        res = 0
        " Go for a paranoid agent: weighted sum of distance to other enemies [inside the circle!] --> greater value if farther away from them "
        for enemy in current_state.enemies:
            if not current_state.enemies[enemy].get('active'):
                res += 1000
        if not current_state.alive:
            res += float("-inf")

        res += 10*len(enemies_in_view)/(sum([manhattan_distance_position_dependend(current_state.position, (current_state.enemies[enemy]['y'], current_state.enemies[enemy]['x'])) for enemy in enemies_in_view])+1)

        #print(current_state) #, "prints result", res, sep=" ")
        #print(enemies_in_view)
        #print("Results in: ", res, sep="", end="\n")
        return res"""
        if current_state.alive:
            return 1000
        else:
            return -1000

    def __repr__(self):
        res = ""
        res += str(self.field) + "\n"
        res += "Field height: " + str(self.field_height) + "\n"
        res += "Field width: " + str(self.field_width) + "\n"
        res += "Actions: " + str(self.actions) + "\n"
        res += "Directions: " + str(self.directions) + "\n"
        res += "Goal: " + str(self.goal) + "\n"
        res += "My ID: " + str(self.our_agent_id) + "\n"
        return res