class _Type:
    def __init__(self, name, starting_health):
        self.name = name
        self.starting_health = starting_health

class _Unit(_Type):
    def __init__(self, name, starting_health):
        self.name = name
        self.starting_health = starting_health

class _Building(_Type):
    def __init__(self, name, starting_health):
        self.name = name
        self.starting_health = starting_health

class Type:
    # Units
    ARCHER = _Unit("ARCHER", 50)
    HORSE = _Unit("HORSE", 50)
    PEASANT = _Unit("PEASANT", 50)
    PIKE = _Unit("PIKE", 50)

    # Buildings
    CASTLE = _Building("CASTLE", 500)
    HOUSE = _Building("HOUSE", 50)

    _name_to_type = {
        "ARCHER": ARCHER,
        "HORSE": HORSE,
        "PEASANT": PEASANT,
        "PIKE": PIKE,

        "CASTLE": CASTLE,
        "HOUSE": HOUSE,
    }

    @classmethod
    def from_string(cls, name):
        return cls._name_to_type[name]
