from .type import Type

class GameConstants:
    MAX_ID = 10000000
    TREE_STARTING_HEALTH = 200
    GOLD_MINE_STARTING_HEALTH = 5000

    LEGAL_BUILDS = set([
        (Type.PEASANT, Type.HOUSE),
        (Type.HOUSE, Type.PEASANT)
    ])

    LEGAL_TRAINS = set([
        (Type.PEASANT, Type.ARCHER),
        (Type.PEASANT, Type.HORSE),
        (Type.PEASANT, Type.PIKE),
    ])

    STARTING_GOLD = 0

    CUT_AMOUNT = 10
    MINE_AMOUNT = 10
