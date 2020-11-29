import numpy as np
from astar import astar_search, null_heuristic
"""
@author David Sebode
@version 1.2
"""


def get_goal(game, state, tactic):
    """
    This is the initializer of the recursive goalfinder algorithm. First the top left and bottom right corner are set
    as the borders of the analysis. A single position to pursue will be returned.
    :param state: Current state of the game
    :param game: Game on which the analysis is done on
    :param tactic: Play offensive (>0) or defensive (<=0)
    :return: A single position on the field
    """
    ul_corner = (0, 0)
    br_corner = (game.field_height - 1, game.field_width - 1)
    return choose_field(game, ul_corner, br_corner, state, tactic)


def choose_field(game, ul_corner, br_corner, state, tactic):
    """
    This method first splits the fields into roughly equal sized fields which will be evaluated. Then the best partial
    field will be chosen to further evaluate. This is done until a field of size 1x1 remains. The algorithm can either
    choose to set a passive or an aggressive playstyle with the tactic parameter. If it is set to values <= 0 fields
    with less enemies will be preferred, else fields with more enemies will be preferred.
    :param game: Current game
    :param ul_corner: Upper left corner of the field that has to be analysed
    :param br_corner: Bottom right corner of the field that has to be analysed
    :param state: Current state of the game
    :param tactic: Offensive or defensive playstyle
    :return: A single position on the field
    """
    if single_field(ul_corner, br_corner):
        return ul_corner
    fields = split_field(ul_corner, br_corner)
    baseline = tactic*999999
    choice = fields[0]
    for field in fields:  # Evaluate all the fields and either choose the first one or the next best one
        if not is_reachable(game, state, get_closest_corner(game, field[0], field[1])):  # Rule out unreachable blocks
            continue
        else:
            temp = evaluate(game, field[0], field[1])
        if tactic <= 0:  #
            if temp > baseline:
                baseline = temp
                choice = field
        else:
            if temp < baseline:
                baseline = temp
                choice = field
    return choose_field(game, choice[0], choice[1], state, tactic)


# Returns true if a field only has one position
def single_field(ul_corner, br_corner):
    """
    Checks if a field is of the size 1x1
    :param ul_corner: Upper left corner of the field
    :param br_corner: Bottom right corner of the field
    :return: True if field has size 1x1 else false
    """
    return br_corner[0] - ul_corner[0] == 1 and br_corner[1] - ul_corner[1] == 1


# Returns the corner that is closest to one of the bound corners
def get_closest_corner(game, ul_corner, br_corner):
    """
    This method checks which corner of the analysed field is closest to one of the corners of the whole play area/field.
    For each corner the distance to the next corner of the field is calculated, e.g. top left corner with upper left
    corner of the partial field etc.
    :param game: Game on which the analysis is based on
    :param ul_corner: Upper left corner of the field
    :param br_corner: Bottom right corner of the field
    :return: A single corner position
    """
    tl_corner = (0, 0)  # top left corner
    tr_corner = (0, game.field_width)  # top right corner
    ll_corner = (game.field_height, 0)  # lower left corner
    lr_corner = (game.field_height, game.field_width)  # lower right corner
    ur_corner = (ul_corner[0], br_corner[1])  # upper right corner of the field to be analysed
    bl_corner = (br_corner[0], ul_corner[1])  # bottom left corner of the field to be analysed

    result = br_corner  # initial starting corner
    temp = sum(list(br_corner))  # initial starting sum for the value of the corner. The lower the better

    if sum(list(np.subtract(ul_corner, tl_corner))) < temp:
        temp = sum(list(np.subtract(ul_corner, tl_corner)))
        result = ul_corner
    if sum(list(np.subtract(bl_corner, ll_corner))) < temp:
        temp = sum(list(np.subtract(bl_corner, ll_corner)))
        result = bl_corner
    if sum(list(np.subtract(tr_corner, ur_corner))) < temp:
        temp = sum(list(np.subtract(tr_corner, ur_corner)))
        result = ur_corner
    if sum(list(np.subtract(lr_corner, br_corner))) < temp:
        result = br_corner
    return result


def evaluate(game, ul_corner, br_corner):
    """
    Assigns a value to the field based on how many positions are taken by enemies are taken by enemies and how many are
    free. The more taken position the field has the worse the value will be.
    :param game: Current game on which the analysis is based
    :param ul_corner: Top right corner of the field
    :param br_corner: Bottom right corner of the field
    :return: A single value for the field
    """
    value = 0
    w, x, y, z = ul_corner[0], ul_corner[1], br_corner[0], br_corner[1]  # Get the coordinates
    while w < y:
        while x < z:
            if not game.field[w][x]:
                value += 1  # Increment the value if the field is empty
            elif game.field[w][x] != game.our_agent_id:
                value -= 1  # Decrease the value if an enemy is in the field
            x += 1
        w += 1
    return value


# Check whether the position is reachable or not
def is_reachable(game, state, position):
    """
    Checks whether a given position can be reached using the A* algorithm
    :param game: Game on which the analysis is based on
    :param state: Current state of the game
    :param position: Position you want to check
    :result: True if the position is reachable, else false
    """
    game.goal = position
    if not astar_search(game, state, null_heuristic):
        return False
    return True


# Split the field into roughly equal sized fields
def split_field(ul_corner, br_corner):
    """
    Split a given field into four roughly equal sub-fields
    :param ul_corner: Upper right corner of the field
    :param br_corner: Bottom right corner of the field
    :return: Four fields consisting of a coordinate for the upper left and bottom right corner
    """
    fields = []
    half_height = br_corner[0] - int((br_corner[0] + ul_corner[0])/2)  # Distance to half the height
    half_width = br_corner[1] - int((br_corner[1] + ul_corner[1])/2)  # Distance to half the width
    fields.append(
        ((ul_corner[0], ul_corner[1]), (ul_corner[0] + half_height, ul_corner[1] + half_width)))  # Upper left quadrant
    fields.append(((ul_corner[0], br_corner[1] - half_width),
                   (ul_corner[0] + half_height, br_corner[1])))  # Upper right quadrant
    fields.append(
        ((br_corner[0] - half_height, ul_corner[1]), (br_corner[0], ul_corner[1] + half_width)))  # Bottom left quadrant
    fields.append(((br_corner[0] - half_height, br_corner[1] - half_width),
                   (br_corner[0], br_corner[1])))  # Bottom right quadrant
    return fields
