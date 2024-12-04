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
        self.dice = [None] * 5
        self._dice_rolls = 0
        self._roll_dice()
        self.scorecards = dict.fromkeys(list(range(0, players)), self._ScoreCard()) # player ID -> scorecard

    upper_section = ['Ones','Twos','Threes'] # upper part of Yahtzee scorecard

    class _ScoreCard:
        def __init__(self):
            self.combinations = dict.fromkeys(Yahtzee.upper_section, None) # combination -> points

    def _roll_dice(self, dice='all'):
        if self._dice_rolls >= 3: return 'dice were rolled three times already'
        if dice == 'all': dice = [0, 1, 2, 3, 4]
        if len(dice) == 0: return 'no selection of dice entered'
        
        for d in dice:
            if type(d) != int or d < 0 or d > 4:
                return 'selection of dice not valid'

        for d in dice:
            self.dice[d] = random.choice([1, 2, 3, 4, 5, 6])
                
        self._dice_rolls += 1

        return None
    
    def _add_points(self, combination):
        combs = self.scorecards[self.current].combinations
        
        if combination not in combs: return 'no such combination'
        if combs[combination] != None: return 'combination was already used'

        if combination in self.upper_section:
            val = self.upper_section.index(combination) + 1
            combs[combination] = self.dice.count(val) * val

        self._rotate_players()

        return None
    

    def _cross_out(self, combination):
        self.dice = [0] * 5
        return self._add_points(combination)
        
    def _rotate_players(self):
        self._dice_rolls = 0
        self._roll_dice()
        self.current = (self.current + 1) % self.players

    def move(self, args, player_id): # override
        """
        Submit a move.

        TODO

        Parameters:
        args (dict): the current player's move
        player_id (int): player ID (unused)

        Returns:
        str: error message in case the move was illegal, None otherwise
        """
        if 'roll_dice' in args:
            return self._roll_dice(args['roll_dice'])
        elif 'score' in args:
            if 'combination' not in args:
                return 'a combination must be passed'
            if args['score'] == 'add points':
                return self._add_points(args['combination'])
            elif args['score'] == 'cross out':
                return self._cross_out(args['combination'])
            else:
                return 'no such score operation'
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
