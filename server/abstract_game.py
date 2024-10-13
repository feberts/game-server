"""
This module provides a base class for games.
"""

class AbstractGame:
    """
    Base class for games.

    This class serves as an abstract base class for games. Every new game must be derived from this class and implement all its methods. These methods will be called by the framework. Furthermore, every new game must be added to the list of available games. See the documentation for details on how to add new games.
    """

    def state(self):
        raise NotImplementedError
        # return <state>

    def move(self):
        raise NotImplementedError
        # return <move valid/illegal and error message>

# TODO
# - min number of player
# - max number of players
