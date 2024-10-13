"""
TODO Kurzbeschreibung des Moduls.

TODO Ausfuehrliche Beschreibung des Moduls, ggf. ueber mehrere Zeilen.
"""

# this module provides an abstract base class for all game classes

class AbstractGame:

    def state(self):
        raise NotImplementedError
        # return <state>

    def move(self):
        raise NotImplementedError
        # return <move valid/illegal and error message>

# TODO
# - min number of player
# - max number of players
