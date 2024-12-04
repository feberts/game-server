"""
Yahtzee game.

This module provides a Yahtzee implementation to be used by the framework.
"""

import random

from abstract_game import AbstractGame

class Yahtzee(AbstractGame):
    """
    Class Yahtzee.

    This class implements a Yahtzee game.
    """

    class _State:
        def __init__(self, players):
            self.current = random.randint(0, players - 1)
            self.gameover = False
            self.players = players

    def __init__(self, players): # override
        """
        Constructor.

        Parameters:
        players (int): number of players
        """
        self._state = self._State(players)

    def move(self, args, player_id): # override
        """
        Submit a move.

        TODO

        Parameters:
        args (dict): the current player's move
        player_id (int): player ID

        Returns:
        str: error message in case the move was illegal, None otherwise
        """
        return None

    def state(self, player_id): # override
        """
        Returns the game state as a dictionary.

        TODO

        Parameters:
        player_id (int): player ID

        Returns:
        dict: game state
        """
        return {'scorecard':{'einser':3, 'zweier':6}}

    def current_player(self): # override
        return [self._state.current]

    def game_over(self): # override
        return self._state.gameover

    def min_players(): # override
        return 1

    def max_players(): # override
        return 8
