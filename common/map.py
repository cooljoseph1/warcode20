import os.path
import json

from .tree import Tree
from .gold_mine import GoldMine
from .robot import Robot

"""
A Map is, well, a map.  It contains information about where gold, trees, and
robots are.
"""

class Map:
    def __init__(self, width, height, board, name=None):
        """
        width:  width of the map
        height:  height of the map
        board:  2d array of things at different locations.
                "T" = tree
                "G" = gold_mine
                "W" = wall
                int = id of robot
        """
        self.width = width
        self.height = height
        self.board = board
        self.name = name or "Unnamed Map"

    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "board": self.board,
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, dic):
        return Map(dic["width"], dic["height"], dic["board"], dic["name"])


def load_map(file_path):
    """
    Load a map from a file path.  Returns a tuple (map, trees, gold_mines, robots)
    of the map, starting trees, starting gold mines, and starting robots.
    """
    data = json.load(file_path)

    map = Map.from_dict(data["map"])
    trees = [Tree.from_dict(tree_info) for tree_info in data["trees"]]
    gold_mines = [GoldMine.from_dict(gold_mine_info) for gold_mine_info in data["gold_mines"]]
    robots = [Robot.from_dict(robot_info) for robot_info in data["robots"]]

    return (map, trees, gold_mines, robots)
