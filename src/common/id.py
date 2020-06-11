import random

from .game_constants import GameConstants

_ids_given = set()

def add_id(id):
    """
    Add an id to our set of id's given.
    """
    _ids_given.add(id)

def random_id():
    """
    Returns a new, random, (almost certainly) unique id.
    """
    for i in range(10):
        id = random.randint(1, GameConstants.MAX_ID)
        if id not in _ids_given:
            break
    add_id(id)
    return id
