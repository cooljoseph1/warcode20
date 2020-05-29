import sys

class Logger:
    def __init__(self, output=None):
        self.output = output or sys.stdout

    def log(self, player, text):
        """
        Logs a piece of text.
        """
        for line in text.split("\n"):
            self.logline(player, line + "\n")

    def log_action(self, player, action):
        self.logline(player, "Action is '" + action + "'\n")

    def logline(self, player, line):
        """
        Logs a line.  Line should end in "\n"
        """

        self.output.write(player.robot.team.to_string() + " player " + str(player.robot.id) + "> " + line)

    def flush(self):
        self.output.flush()
