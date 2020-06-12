# Warcode 2020
## Introduction
Warcode is an AI competition similar to Battlecode.  In Warcode, competitors
create AIs to play a game similar to Starcraft or Warcraft, communicating with
the engine via standard input and output.  In theory, any language could be used
to write an AI, but currently only Python is supported.

## Specs
You can find the specs in the file [specs.md](specs.md).

## Getting Started
First, make sure you have `git` and Python 3.6 installed on your system.  If you
don't have them installed, do so now.

Then, clone this repository by opening a terminal and running
```bash
git clone https://github.com/cooljoseph1/warcode20.git
```
`cd` into the newly created directory, and run
```bash
python3 setup.py test
```
to make sure everything is working.  If this does not work, double check that
you have added python to your PATH variable before contacting the devs.  
Note:  On Windows you will likely need to use `python setup.py test`.

If all of the tests succeeded in the previous step, you are ready to test out a
bot.  In the same directory you ran tests, run
```bash
python3 -m warcode.runner
```
This should open a window (created using Tkinter) which you can run games in.
Test it out by creating a new game of `samplebot` vs `samplebot` on any of the
maps provided.  Uncheck the box to run it sandboxed.  If it all works, you're
ready to get coding!

#### Other useful modules
1. `warcode.map_creator` -- This module is used to make custom maps.
2. `warcode.engine` -- You can use this module to run a game on the command line.

## Creating a bot
All bots must be saved in the `bots` directory.  They must be completely
contained inside a single folder titled the bot's name.  (Nesting folders is
okay.)

Inside of the folder must be a text file named `language` (no extension),
containing the language of the bot.  Right now the only acceptable language is
"python", denoting Python 3.6.

Additionally, there must be a file named `main.py`.  This is the file that will
be executed whenever a robot is created.  It will receive input through stdin on
game information and must output its actions via stdout.  This is explained in
more depth in the specs.

`samplebot` is a bot provided to you to show how to format your code.  Included
in it is a module named `python_starter`.  This module does the communicating
with the engine, so you as a programmer need only worry about coding your bot.
It is highly recommended (but not necessary) to include this module with your
own code.  Documentation for this module can be found at `apis/python_api.md`.

## Competing
Currently, the plan is to hold a double elimination tournament on TBD.  To
participate in it, submit your bot via TBD by TBD.  There will not be prizes.
