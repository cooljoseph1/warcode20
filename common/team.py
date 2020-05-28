from enum import Enum

class Team(Enum):
    RED = "RED"
    BLUE = "BLUE"

    def to_string(self):
        return self.value

    @classmethod
    def from_string(cls, team):
        if team == "RED":
            return cls.RED
        if team == "BLUE":
            return cls.BLUE
        raise ValueError("'" + team + "' is not a valid team.  Only 'RED' and 'BLUE' are allowed.")
