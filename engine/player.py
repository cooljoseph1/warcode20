from subprocess import Popen, PIPE
import os.path
import psutil
import time
import traceback

from ..common.errors import LanguageError

class Player:
    """
    A Player runs a competitor's code for a certain robot
    """
    def __init__(self, path_to_code, language, robot):
        """
        Start a player's code
        """

        self.robot = robot

        if language == "python":
            command = ["python", os.path.join(path_to_code, "main.py")]
        else:
            raise LanguageError("Sorry, but " + language + " is not supported.")

        # Create a process.  The PIPE's are used to communicate to stdin and get
        # the stdout and stderr.
        self.process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        # Used to pause and resume the process
        self.ps_process = psutil.Process(self.process.pid)
        self.pause()


    def run_turn(self, input, time_limit=20, logger=None):
        """
        Runs the player's code for a turn, returning the actions the player takes.

        input:  A single line, ending with "\n", to print to the player's stdin
                before the player runs its code.  It should be a json encoded
                object.
        time_limit:  Time limit, in milliseconds, for player to output action.
                If not printed in that time, the player is killed.
        """
        try:
            self.process.stdin.write(input)
            self.unpause()

            start_time = time.time()
            while time.time() < start_time + time_limit / 1000:
                # Print out stderr from the player
                if logger:
                    for line in iter(process.stderr.readline, b''):
                        logger.logline(self, line)

                line = process.stdout.readline()
                if line:
                    self.pause()
                    return line
                time.sleep(0.0001) # Sleep for 0.1 ms

            self.pause()
        except:
            if logger:
                logger.log(traceback.format_exc())
        finally:
            # Kill the robot if the player doesn't return in time or throws an
            # error
            return "EXPLODE"

    def pause(self):
        """
        Pause the execution of the player's code.
        """
        self.ps_process.suspend()

    def unpause(self):
        """
        Resume the execution of  the player's code.
        """
        self.ps_process.resume()

    def kill_process(self):
        """
        Kill our process
        """
        self.process.kill()
