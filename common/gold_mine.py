from .game_constants import GameConstants

class GoldMine:
    def __init__(self, x, y, health=None):
        self.x = x
        self.y = y
        self.health = health if health is not None else GameConstants.GOLD_MINE_STARTING_HEALTH
