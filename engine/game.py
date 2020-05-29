import sys
import random

from ..common import Map, Team, load_map, GameConstants, Robot
from .player import Player
from .logger import Logger


class Game:
    def __init__(self, map_name, player1_dir, player2_dir,
                 language1="python", language2="python", debug=False):
        """
        Initialize the game.
        map_name:  name of the map to play on
        player1_dir:  path to the directory containing the first player's code
        player2_dir:  path to the directory containing the second player's code
        language1:  the language player1 is written in
        language2:  the language player2 is written in
        debug:  print out debug outputs
        """
        self.map, self.trees, self.gold_mines, robots = load_map(map_name)
        self.player1_dir = player1_dir
        self.player2_dir = player2_dir
        self.language1 = language1
        self.language2 = language2

        self.ids_given = {robot.id for robot in robots}

        self.players = [
            self.create_player(robot)
            for robot in robots
        ]
        
        self.gold = {"RED": GameConstants.STARTING_GOLD, "BLUE": GameConstants.STARTING_GOLD}
        self.wood = {"RED": GameConstants.STARTING_WOOD, "BLUE": GameConstants.STARTING_WOOD}

        self.logger = Logger(sys.stdout) if debug else None

        self.going = False
        self.turn = 0
        self.winner = None

    def run(self):
        """
        Run the game.
        """
        self.going = True
        self.turn = 1

        self.run_turn()
        while self.going:
            self.turn += 1
            self.run_turn()

        self.winner = self.get_winner()
        return self.winner

    def create_player(self, robot):
        """
        Creates a player from a robot.
        """
        return (
            Player(self.player1_dir, self.language1, robot)
            if robot.team is Team.RED else
            Player(self.player2_dir, self.language2, robot)
        )

    def new_id(self, max=1000000):
        """
        Returns a new, random, (almost certainly) unique id.
        """
        for i in range(10):
            id = random.randint(1, max)
            if id not in ids_given:
                ids_given.add(id)
                return id
        return random.randint(1, max)

    def run_turn(self):
        """
        Run a single turn in the game.
        """
        for player in self.players[:]:
            if player.robot.health <= 0:
                continue
            # Player gets x5 time on the first turn.
            time_multiplier = 5 if player.turns_taken == 0 else 1
            action = player.run_turn(self.get_input(player.robot),
                                     time_limit=player.robot.type.time_limit * time_multiplier,
                                     debug=self.debug)
            self.process_action(action, player.robot)
        self.remove_dead_players()
        self.check_over()

    def process_action(self, action, player):
        """
        Process an action taken by a player.
        """

        if self.logger:
            self.logger.log_action(action)

        tokens = action.strip().split()
        try:
            if tokens[0] == "ATTACK":
                x, y = int(tokens[1]), int(tokens[2])
                self.attack(player, x, y)
                return
            if tokens[0] == "BUILD":
                x, y = int(tokens[1]), int(tokens[2])
                type = Type.from_string(tokens[3])
                self.build(player, x, y, type)
                return
            if tokens[0] == "CUT":
                tree_id = int(tokens[1])
                self.cut(player, tree_id)
                return
            if tokens[0] == "EXPLODE":
                self.kill(player)
                return
            if tokens[0] == "MINE":
                gold_mine_id = int(tokens[1])
                self.mine(player, gold_mine_id)
                return
            if tokens[0] == "MOVE":
                x, y = int(tokens[1]), int(tokens[2])
                self.move(player, x, y)
                return
            if tokens[0] == "TRAIN":
                type = Type.from_string(tokens[1])
                self.train(player, type)
                return
        finally:
            if self.logger:
                self.logger.log("Invalid action: " + action)

    def remove_dead_players(self):
        self.players = [player for player in self.players if player.robot.health > 0]

    def kill(self, player):
        """
        Kills a player's robot, but does not remove it from our list of players
        """
        player.robot.health = 0
        self.map.board[player.robot.y][player.robot.x] = " "
        player.kill_process()

    def kill_tree(self, tree):
        """
        Removes a tree.  A tree becomes an empty space when it dies.
        """
        tree.health = 0
        self.map.board[tree.y][tree.x] = " "
        self.trees.remove(tree)

    def kill_gold_mine(self, gold_mine):
        """
        Removes a gold mine.  A gold mine turns into a wall when it is destroyed.
        """
        gold_mine.health = 0
        self.map.board[gold_mine.y][gold_mine.x] = "W"
        self.gold_mines.remove(gold_mine)

    def attack(self, player, x, y):
        """
        Have the player attack the position (x, y).
        """
        if not self.map.is_on_the_map(x, y):
            if self.logger:
                self.logger.log(player, "Cannot ATTACK: ({}, {}) is off the map.".format(x, y))
            return

        if player.robot.type.attack_radius < (x - player.robot.x) ** 2 + (y - player.robot.y) ** 2:
            if self.logger:
                self.logger.log(
                    player, "Cannot ATTACK: ({}, {}) is too far from current location.".format(x, y))
            return

        for player2 in self.players[:]:
            if (player2.robot.x - x) ** 2 + (player2.robot.y - y) ** 2 <= player.robot.damage_radius:
                player2.robot.health -= player.robot.attack_damage
                if player2.robot.health <= 0:
                    self.kill(player2)

        # Trees get harmed by attacks, but gold mines do not.
        for tree in self.trees[:]:
            if (tree.x - x) ** 2 + (tree.y - y) ** 2 <= player.robot.damage_radius:
                tree.health -= player.robot.attack_damage
                if tree.health <= 0:
                    self.kill_tree(tree)

    def build(self, player, x, y, type):
        """
        Have the player build a robot of the given type at the position (x, y).
        """
        if (player.robot.type, type) not in GameConstants.LEGAL_BUILDS:
            if self.logger:
                self.logger.log(player, "Cannot BUILD: A {} cannot build a {}.".format(
                    player.robot.type, type))
            return

        if not self.map.is_on_the_map(x, y):
            if self.logger:
                self.logger.log(player, "Cannot BUILD: ({}, {}) is off the map.".format(x, y))
            return

        if (x - player.robot.x) ** 2 + (y - player.robot.y) ** 2 > 2:
            if self.logger:
                self.logger.log(
                    player, "Cannot BUILD: ({}, {}) is not adjacent to the robot.".format(x, y))
            return

        if self.map.board[y][x] != " ":
            if self.logger:
                self.logger.log(player, "Cannot BUILD: ({}, {}) is not empty.".format(x, y))
            return

        if self.get_gold(player.robot.team) < type.gold_cost:
            if self.logger:
                self.logger.log(player, "Cannot BUILD:  Insufficient gold.")
            return

        if self.get_wood(player.robot.team) < type.wood_cost:
            if self.logger:
                self.logger.log(player, "Cannot BUILD:  Insufficient wood.")
            return

        self.add_gold(player.robot.team, -type.gold_cost)
        self.add_wood(player.robot.team, -type.wood_cost)

        new_robot = Robot(self.new_id(), x, y, player.robot.team, type)
        new_player = self.create_player(new_robot)
        self.map.board[new_player.robot.y][new_player.robot.x] = new_player.robot.id
        self.players.append(new_player)

    def cut(self, player, tree_id):
        """
        Have the player cut a tree to gather wood.
        """
        if player.robot.type is not Type.PEASANT:
            if self.logger:
                self.logger.log(player, "Cannot CUT:  Robot is not a PEASANT.")
            return

        tree = None
        for tree2 in self.trees:
            if tree2.id == tree_id:
                tree = tree2
                break

        if tree is None:
            if self.logger:
                self.logger.log(
                    player, "Cannot CUT:  No tree with id {} does exists.".format(tree_id))
            return

        if (player.robot.x - tree.x) ** 2 + (player.robot.y - tree.y) ** 2 > 2:
            if self.logger:
                self.logger.log(player, "Cannot CUT:  Robot is not adjacent to tree.")
            return

        # Always get CUT_AMOUNT of wood, even if the tree is almost dead.
        self.add_wood(player.robot.team, GameConstants.CUT_AMOUNT)
        tree.health -= GameConstants.CUT_AMOUNT
        if tree.health <= 0:
            self.kill_tree(tree)

    def mine(self, player, gold_mine_id):
        """
        Have the player mine a gold mine to receive gold.
        """
        if player.robot.type is not Type.PEASANT:
            if self.logger:
                self.logger.log(player, "Cannot BUILD:  Robot is not a PEASANT.")
            return

        gold_mine = None
        for gold_mine2 in self.trees:
            if gold_mine2.id == gold_mine_id:
                gold_mine = gold_mine2
                break

        if gold_mine is None:
            if self.logger:
                self.logger.log(
                    player, "Cannot MINE:  No gold mine with id {} does exists.".format(gold_mine_id))
            return

        if (player.robot.x - gold_mine.x) ** 2 + (player.robot.y - gold_mine.y) ** 2 > 2:
            if self.logger:
                self.logger.log(player, "Cannot MINE:  Robot is not adjacent to mine.")
            return

        # Always get MINE_AMOUNT of gold, even if the gold mine is almost deplenished.
        self.add_gold(player.robot.team, GameConstants.MINE_AMOUNT)
        gold_mine.health -= GameConstants.MINE_AMOUNT
        if gold_mine.health <= 0:
            self.kill_gold_mine(gold_mine)

    def move(self, player, x, y):
        """
        Move a player's robot to the position (x, y).
        """
        if not player.robot.type.is_unit():
            if self.logger:
                self.logger.log(player, "Cannot MOVE: Only units can move.")
            return

        if not self.map.is_on_the_map(x, y):
            if self.logger:
                self.logger.log(player, "Cannot MOVE: ({}, {}) is off the map.".format(x, y))
            return

        if player.robot.type.move_radius < (x - player.robot.x) ** 2 + (y - player.robot.y) ** 2:
            if self.logger:
                self.logger.log(
                    player, "Cannot MOVE: ({}, {}) is too far from current location.".format(x, y))
            return

        if self.board[y][x] != " ":
            if self.logger:
                self.logger.log(
                    player, "Cannot MOVE: ({}, {}) is a wall or is occupied.".format(x, y))
            return

        self.map.board[player.robot.y][player.robot.x] = " "
        self.map.board[y][x] = player.robot.id

    def train(self, player, type):
        """
        Have a peasant train to a new type.
        """
        if (player.robot.type, type) not in GameConstants.LEGAL_TRAINS:
            if self.logger:
                self.logger.log(player, "Cannot TRAIN: A {} cannot train to become a {}.".format(
                    player.robot.type, type))
            return

        if self.get_gold(player.robot.team) < type.gold_cost:
            if self.logger:
                self.logger.log(player, "Cannot TRAIN: Insufficient gold.")
            return

        if self.get_wood(player.robot.team) < type.wood_cost:
            if self.logger:
                self.logger.log(player, "Cannot TRAIN: Insufficient wood.")
            return

        self.add_gold(player.robot.team, -type.gold_cost)
        self.add_wood(player.robot.team, -type.wood_cost)

        player.robot.type = type
        player.robot.health = type.starting_health

    def check_over(self):
        """
        Checks if the game is over.  End conditions are that only one team has
        units left or that there has been 1000 turns.
        """
        if self.turn >= 1000:
            self.going = False
            return

        if all(player.robot.team is Team.RED for player in self.players):
            self.going = False
            return

        if all(player.robot.team is Team.BLUE for player in self.players):
            self.going = False
            return

    def get_winner(self):
        """
        Returns the winner of the game.
        Order of tiebreaks:
        1. Team with most total health for its units.
        2. Team with more gold.
        3. Team with more wood.
        4. Team with highest unit id.
        """
        if self.going:
            return None

        red_players = [player for player in players if player.robot.team is Team.RED]
        blue_players = [player for player in players if player.robot.team is Team.BLUE]

        red_score = sum(player.robot.health for player in red_players)
        blue_score = sum(player.robot.health for player in blue_players)

        if red_score > blue_score:
            return Team.RED
        if blue_score > red_score:
            return Team.BLUE

        if self.gold["RED"] > self.gold["BLUE"]:
            return Team.RED
        if self.gold["BLUE"] > self.gold["RED"]:
            return Team.BLUE
        if self.wood["RED"] > self.wood["BLUE"]:
            return Team.RED
        if self.wood["BLUE"] > self.wood["RED"]:
            return Team.BLUE

        highest_red_id = max(player.robot.id for player in red_team)
        highest_blue_id = max(player.robot.id for player in blue_team)

        if highest_red_id > highest_blue_id:
            return Team.RED
        return Team.BLUE

    def get_gold(self, team):
        return self.gold["RED"] if team is Team.RED else self.gold["BLUE"]

    def get_wood(self, team):
        return self.wood["RED"] if team is Team.RED else self.wood["BLUE"]

    def add_gold(self, team, amount):
        if team is Team.RED:
            self.gold["RED"] += amount
        else:
            self.gold["BLUE"] += amount

    def add_wood(self, team, amount):
        if team is Team.RED:
            self.wood["RED"] += amount
        else:
            self.wood["BLUE"] += amount
