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

    def __init__(self, players): # override
        """
        Constructor.

        Parameters:
        players (int): number of players
        """
        self._state = self._State(players)

    class _State:
        def __init__(self, players):
            self.current = random.randint(0, players - 1)
            self.gameover = False
            self.players = players
            self.dice = [random.choice([1, 2, 3, 4, 5, 6]) for _ in range(5)]
            self.scorecards = dict.fromkeys(list(range(0, players)), Yahtzee._ScoreCard()) # player ID -> scorecard

    class _ScoreCard:
        def __init__(self):
            self.combinations = dict.fromkeys(['Ones','Twos','Threes'], None) # combination -> score




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
        return {'scorecard':self._state.scorecards[player_id].combinations, 'dice':self._state.dice}

    def current_player(self): # override
        return [self._state.current]

    def game_over(self): # override
        return self._state.gameover

    def min_players(): # override
        return 1

    def max_players(): # override
        return 8
