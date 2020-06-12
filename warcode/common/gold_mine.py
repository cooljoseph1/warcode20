from .game_constants import GameConstants
from .id import add_id, random_id

class GoldMine:
    def __init__(self, x, y, health=None, id=None):
        self.x = x
        self.y = y
        self.health = health if health is not None else GameConstants.GOLD_MINE_STARTING_HEALTH
        self.id = id or random_id()
        add_id(self.id)

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "health": self.health,
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, dic):
        return GoldMine(dic["x"], dic["y"], dic["health"], dic["id"])
