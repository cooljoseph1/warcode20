from .team import Team
from .type import Type

class Robot:
    def __init__(self, x, y, type, team, health=None):
        self.x = x
        self.y = y
        self.team = team
        self.type = type
        self.health = health or self.type.starting_health

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "type": self.type.to_string(),
            "team": self.team.to_string(),
            "health": self.health,
        }

    @classmethod
    def from_dict(cls, dic):
        return cls(dic["x"], dic["y"], Type.from_string(dic["type"]),
                Team.from_string(dic["team"]), dic["health"])
