class _Type:
    def __init__(self, name, gold_cost, wood_cost, starting_health, vision_radius, time_limit):
        """
        name:  name of robot type
        starting_health:  initial health of robot
        vision_radius:  radius within which robot can see
        time_limit:  time limit per turn for robot to run its code.  First turn
                has x5 the time.
        """
        self.name = name
        self.gold_cost = gold_cost
        self.wood_cost = wood_cost
        self.starting_health = starting_health
        self.vision_radius = vision_radius
        self.time_limit = time_limit

    def is_unit(self):
        return False

    def is_building(self):
        return False

    def to_string(self):
        return self.name

class _Unit(_Type):
    def __init__(self, name, gold_cost, wood_cost, starting_health, vision_radius, move_radius,
            attack_radius, damage_radius, attack_damage, time_limit):
        """
        name:  name of unit type
        cost:  cost to build the unit
        starting_health:  initial health of unit
        vision_radius:  radius within which unit can see
        move_radius:  radius within which the unit can move
        attack_radius:  radius within which the unit can attack
        damage_radius:  size of "explosion" created by attack
        attack_damage:  damage done to units within damage_radius of attack
        time_limit:  time limit per turn for unit to run its code.  First turn
                has x5 the time.
        """
        super().__init__(name, gold_cost, wood_cost, starting_health, vision_radius, time_limit)
        self.move_radius = move_radius
        self.attack_radius = attack_radius
        self.damage_radius = damage_radius
        self.attack_damage = attack_damage

    def is_unit(self):
        return True

    def is_building(self):
        return False

class _Building(_Type):
    def __init__(self, name, gold_cost, wood_cost, starting_health, vision_radius, time_limit):
        """
        name:  name of building type
        starting_health:  initial health of building
        vision_radius:  radius within which building can see
        time_limit:  time limit per turn for building to run its code.  First turn
                has x5 the time.
        """
        super().__init__(name, gold_cost, wood_cost, starting_health, vision_radius, time_limit)

    def is_unit(self):
        return False

    def is_building(self):
        return True

class Type:
    # Units
    ARCHER = _Unit("ARCHER", 80, 50, 50, 150, 2, 80, 0, 10, 20)
    HORSE = _Unit("HORSE", 150, 100, 100, 80, 5, 1, 0, 30, 20)
    PEASANT = _Unit("PEASANT", 50, 20, 50, 60, 2, -1, -1, 0, 20)
    PIKE = _Unit("PIKE", 100, 120, 150, 80, 1, 5, 0, 10, 20)

    # Buildings
    HOUSE = _Building("HOUSE", 500, 800, 300, 100, 20)

    ALL_TYPES = [
        ARCHER,
        HORSE,
        PEASANT,
        PIKE,
        HOUSE,
    ]

    _name_to_type = {
        "ARCHER": ARCHER,
        "HORSE": HORSE,
        "PEASANT": PEASANT,
        "PIKE": PIKE,
        "HOUSE": HOUSE,
    }

    @classmethod
    def from_string(cls, name):
        return cls._name_to_type[name]
