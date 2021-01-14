class GameState:
    def __init__(self, position, direction, active, speed):
        self.position = position
        self.direction = direction
        self.alive = active
        self.speed = speed
        self.enemies = {}  # enemie id: ( (x, y), direction )

    def calculate_next_action(self):
        pass

    def is_win(self, enemy_in_bounds):
        """ Has to be changed? """
        for enemy in enemy_in_bounds:
            if self.enemies[enemy]['active']:
                return False
        return True

    def get_enemy_within_bounds(self, bound1, bound2):
        """
        Method to get all enemies within a certain bound; Here bound are to positions.\n
        Consider the following example:

        [0, 2, 0, 0, 0, 0, 0, 0]\n
        [0, 2, 2, 2, 0, 1*,0, 0]\n
        [0, 0, 0, 2*,0, 1, 0, 0]\n
        [0, 0, 0, 0, 0, 1, 0, 0]\n
        [0, 0, 0, 0, 0, 1, 0, 0]\n

        Current agents position is: (1, 5)\n
        We want to know if there are enemies within (0, 2), (3, 6)

        [0, 2, 0, 3, 3, 3, 3, 0]\n
        [0, 2, 2, 3, 3, 3, 3, 0]\n
        [0, 0, 0, 3, 3, 3, 3, 0]\n
        [0, 0, 0, 0, 0, 1, 0, 0]\n
        [0, 0, 0, 0, 0, 1, 0, 0]\n

        If any enemy is now within the 3's his ID will be yield.
        In this case, 2 was within the 3s-grid so we will return ['2']

        :param bound1: A position containing solely y-position; (y1, y2)
        :param bound2: A position containing solely x-position; (x1, x2)
        :return: All enemies ID in a list
        """
        enemy_in_bounds = []
        for enemy in self.enemies:
            y = self.enemies[enemy].get('y')
            x = self.enemies[enemy].get('x')
            if bound1[0] <= y <= bound1[1] and bound2[0] <= x <= bound2[1]:
                enemy_in_bounds.append(enemy)
        return enemy_in_bounds

    def __repr__(self):
        res = "Position: " + str(self.position) + "\n"
        res += "Direction: " + self.direction + "\n"
        res += "Active|Alive: " + str(self.alive) + "\n"
        res += "Speed: " + str(self.speed) + "\n"
        res += "Enemy data: " + str(self.enemies) + "\n"
        return res
