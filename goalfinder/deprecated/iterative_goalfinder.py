import numpy as np

# wx 0 0
# 0 0 0
# 0 0 yz

"""
@Deprecated
"""
# Split the game_field and return a bunch of tuples for the coordinates of the squares
# Scale determines the size of the field
def split_field(game, scale):
    field_list = []
    w, x = 0, 0
    y, z = scale, scale
    if game.field_width % scale != 0:
        scale += 1
    while y <= game.field_height:
        while z <= game.field_width:
            field_list.append((w, x, y, z))
            x += scale
            z += scale
        x = 0
        z = 0
        w += scale
        y += scale
    return field_list


# Evaluate the value of a field. The more empty the field, the more points it gets
# w, x: upper left bound; y,z lower right bound
# Increase the value if the field is empty, decrease if an enemy is blocking the position
def evaluate(game, w, x, y, z):
    value = 0
    while w < y:
        while x < z:
            if not game.field[w][x]:
                value += 1
            elif game.field[w][x] != game.our_agent_id:
                value -= 1
            x += 1
        w += 1
    return value


# Choose a random position in the field
def choose_rand_pos(w, x, y, z):
    return tuple([np.random.randint(w, y), np.random.randint(x, z)])


# Choose the field with the highest value and return the corner coordinates
def choose_field(game, fields, tactic):
    result = game.field
    baseline = 999999*tactic
    if tactic < 0:
        for field in fields:
            temp = evaluate(game, field[0], field[1], field[2], field[3])
            if temp > baseline:
                baseline = temp
                result = field
    else:
        for field in fields:
            temp = evaluate(game, field[0], field[1], field[2], field[3])
            if temp < baseline:
                baseline = temp
                result = field
    return result


# Get the goal of the player using the field, player_id, width and height of the field
# Scale is the size of the subfields to be analysed. The smaller the scale, the more accurate the evaluation
def get_goal(game, scale, tactic):
    split_fields = split_field(game, scale)
    goal_field = choose_field(game, split_fields, tactic)
    return choose_rand_pos(goal_field[0], goal_field[1], goal_field[2], goal_field[3])
