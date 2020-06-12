import random

from .team import Team
from .type import Type
from .id import add_id, random_id

class Robot:
    def __init__(self, x, y, type, team, health=None, id=None):
        self.x = x
        self.y = y
        self.team = team
        self.type = type
        self.health = health or self.type.starting_health
        self.id = id or random_id()
        add_id(self.id)

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "type": self.type.to_string(),
            "team": self.team.to_string(),
            "health": self.health,
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, dic):
        return cls(dic["x"], dic["y"], Type.from_string(dic["type"]),
                Team.from_string(dic["team"]), dic["health"], dic["id"])
