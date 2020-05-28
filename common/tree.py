from .game_constants import GameConstants

class Tree:
    def __init__(self, x, y, health=None):
        self.x = x
        self.y = y
        self.health = health if health is not None else GameConstants.TREE_STARTING_HEALTH

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "health": self.health
        }

    @classmethod
    def from_dict(cls, dic):
        return cls(dic["x"], dic["y"], dic["health"])
