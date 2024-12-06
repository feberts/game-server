"""
Yahtzee game.

This module provides a Yahtzee implementation to be used by the framework.
"""

import random

from abstract_game import AbstractGame

#TODO make some attributes functions private
#TODO mit 1,2 und 3 clients testen
# TODO NOTEs entfernrn

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
        self._current = list(range(0, players)) # random.randint(0, players - 1) # NOTE neu
        self._gameover = False
        self._players = players
        self._scorecards = {} # player ID -> scorecard
        self._init_scorecards()
        self._dice = [None] * 5
        self._dice_rolls = 0
        self._roll_dice()
        self._ranking = {} # name -> total points

    # upper and lower sections of Yahtzee scorecard:
    _upper_section = ['Ones', 'Twos', 'Threes']
    _lower_section = []

    def _init_scorecards(self):
        for player_id in range(0, self._players):
            self._scorecards[player_id] = self._ScoreCard()

    class _ScoreCard:
        def __init__(self):
            self.player_name = None
            self.categories = dict.fromkeys(Yahtzee._upper_section
                                              + Yahtzee._lower_section,
                                              None) # category -> points
            
        def full(self):
            full = True
            for point in self.categories.values():
                if point == None:
                    full = False
                    break
            return full
        
        def total_points(self):
            points = 0
            for point in self.categories.values():
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
            self._dice[d] = random.choice([1, 2, 3, 4, 5, 6])
                
        self._dice_rolls += 1

        return None
    
    def _add_points(self, category):
        if category in self._upper_section:
            face_value = self._upper_section.index(category) + 1
            count = self._dice.count(face_value)
            if count == 0: return f'there are no {face_value}s'
            points = count * face_value
            return self._update_scorecard(category, points)
        else:
            # NOTE implement lower section of Yahtzee scorecard here
            return 'not implemented'

    def _update_scorecard(self, category, points):
        combs = self._scorecards[self._current].categories
        
        if category not in combs: return 'no such category'
        if combs[category] != None: return 'category was already used'
    
        combs[category] = points
        self._check_game_over()

        if self._gameover:
            self._current = []
            self._build_ranking()
        else:
            self._rotate_players()
        
        return None

    def _build_ranking(self):
        for sc in self._scorecards.values():
            self._ranking[sc.player_name] = sc.total_points()
        
    def _check_game_over(self):
        over = True
        for sc in self._scorecards.values():
            if not sc.full():
                over = False
                break
        self._gameover = over
            

    def _cross_out(self, category):
        return self._update_scorecard(category, 0)
        
    def _rotate_players(self):
        self._dice_rolls = 0
        self._roll_dice()
        self._current = (self._current + 1) % self._players

    def _set_name(self, name, player_id):
        if not name:
            return 'name must not be empty'
    
        if self._scorecards[player_id].player_name:
            return 'you cannot change your name'

        for sc in self._scorecards.values():
            if sc.player_name == name:
                return 'name already in use'
        
        self._scorecards[player_id].player_name = name
        self._current.remove(player_id) # NOTE neu
        if not self._current: self._current = random.randint(0, self._players - 1) # NOTE neu
        
        return None
    
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
            if 'category' not in args:
                return 'a category must be passed'
            if args['score'] == 'add points':
                return self._add_points(args['category'])
            elif args['score'] == 'cross out':
                return self._cross_out(args['category'])
            else:
                return 'no such score operation'
        elif 'name' in args:
            return self._set_name(args['name'], player_id)
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
        state = {'scorecard':self._scorecards[player_id].categories}

        if self._gameover:
            state['ranking'] = self._ranking
        else:
            state['dice'] = self._dice
            
        return state

    def current_player(self): # override
        if type(self._current) == list:
            return self._current
        else:
            return [self._current]

    def game_over(self): # override
        return self._gameover

    def min_players(): # override
        return 1

    def max_players(): # override
        return 8
