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
        self.ranking = {} # name -> total points

    upper_section = ['Ones', 'Twos', 'Threes'] # upper part of Yahtzee scorecard

    class _ScoreCard:
        def __init__(self):
            self.combinations = dict.fromkeys(Yahtzee.upper_section, None) # combination -> points
            self.player_name = 'Bob'
            
        def full(self):
            full = True
            for point in self.combinations.values():
                if point == None:
                    full = False
                    break
            return full
        
        def total_points(self):
            points = 0
            for point in self.combinations.values():
                points += point
            return points

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
        if combination in self.upper_section:
            face_value = self.upper_section.index(combination) + 1
            count = self.dice.count(face_value)
            if count == 0: return f'there are no {face_value}s'
            points = count * face_value
            return self._update_scorecard(combination, points)
        else:
            # implement lower section of Yahtzee scorecard here
            return None

    def _update_scorecard(self, combination, points):
        combs = self.scorecards[self.current].combinations
        
        if combination not in combs: return 'no such combination'
        if combs[combination] != None: return 'combination was already used'
    
        combs[combination] = points

        self._check_game_over()

        if self.gameover:
            self.current = []
            self._build_ranking()
        else:
            self._rotate_players()
        
        return None

    def _build_ranking(self):
        for sc in self.scorecards.values():
            self.ranking[sc.player_name] = sc.total_points()
        
    def _check_game_over(self):
        over = True
        for sc in self.scorecards.values():
            if not sc.full():
                over = False
                break
        self.gameover = over
            

    def _cross_out(self, combination):
        return self._update_scorecard(combination, 0)
        
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
        state = {'scorecard':self.scorecards[player_id].combinations}

        if self.gameover:
            state['ranking'] = self.ranking
        else:
            state['dice'] = self.dice
            
        return state

    def current_player(self): # override
        if type(self.current) == list:
            return self.current
        else:
            return [self.current]

    def game_over(self): # override
        return self.gameover

    def min_players(): # override
        return 1

    def max_players(): # override
        return 8
