import json

from ..common import Robot, GoldMine, Tree

class MapData:
    def __init__(self, width=30, height=30, name="Untitled", save_file=None):
        if save_file is not None:
            self.load(self.save_file)
            return

        self.name = name
        self.width = width
        self.height = height
        self.save_file = save_file

        self.map = [[" " for x in range(width)] for y in range(height)]
        self.gold_mines = []
        self.trees = []
        self.robots = []

    def load(self, file):
        self.save_file = file
        with open(self.save_file) as f:
            data = json.load(f)

        self.name = data["name"]
        self.width = data["width"]
        self.height = data["height"]
        self.map = data["map"]
        self.gold_mines = {gold_mine_info["id"]: GoldMine.from_dict(gold_mine_info) for gold_mine_info in data["gold_mines"]}
        self.trees = {tree_info["id"]: Tree.from_dict(tree_info) for tree_info in data["trees"]}
        self.robots = {robot_info["id"]: Robot.from_dict(robot_info) for robot_info in data["robots"]}

    def save(self, file=None):
        self.save_file = file or self.save_file
        with open(self.save_file) as f:
            json.dump(self.to_dict())

    def to_dict(self):
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "map": self.map,
            "gold_mines": self.gold_mines,
            "trees": self.trees,
            "robots": self.robots,
        }
