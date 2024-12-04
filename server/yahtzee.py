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
        Parameters:
        players (int): number of players
        """
        self.current = random.randint(0, players - 1)
        self.gameover = False
        self.players = players
        self.dice = []
        self._roll_dice()
        self.scorecards = dict.fromkeys(list(range(0, players)), self._ScoreCard()) # player ID -> scorecard

    class _ScoreCard:
        def __init__(self):
            self.combinations = dict.fromkeys(['Ones','Twos','Threes'], None) # combination -> score

    def _roll_dice(self, dice=None):
        self.dice = [random.choice([1, 2, 3, 4, 5, 6]) for _ in range(5)]


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
        if 'roll' in args:
            self._roll_dice()
        else:
            return 'no such move'
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
        return {'scorecard':self.scorecards[player_id].combinations, 'dice':self.dice}

    def current_player(self): # override
        return [self.current]

    def game_over(self): # override
        return self.gameover

    def min_players(): # override
        return 1

    def max_players(): # override
        return 8
