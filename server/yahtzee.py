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
        self._current = list(range(0, players))
        self._gameover = False
        self._players = players
        self._scorecards = {} # player ID -> scorecard
        self._init_scorecards()
        self._dice = [None] * 5
        self._dice_rolls = 0
        self._roll_dice()
        self._ranking = {} # name -> total points

    # upper and lower sections of Yahtzee scorecard:
    # (according to https://en.wikipedia.org/w/index.php?title=Yahtzee&oldid=1258193803)
    _upper_section = ['Ones', 'Twos', 'Threes'] # NOTE add more categories here
    _lower_section = [] # NOTE add more categories here

    class _ScoreCard:
        """
        This class implements a Yahtzee scorecard.
        """
        def __init__(self):
            self.player_name = None
            self.categories = dict.fromkeys(
                Yahtzee._upper_section + Yahtzee._lower_section, None) # category -> points

        def full(self):
            """
            Determine whether the scorecard is filled completely or not.
            """
            full = True
            for point in self.categories.values():
                if point == None:
                    full = False
                    break
            return full

        def total_points(self):
            """
            Calculate total points.
            """
            return sum(self.categories.values())

    def _init_scorecards(self):
        """
        Assigning a scorecard to every player.
        """
        for player_id in range(0, self._players):
            self._scorecards[player_id] = self._ScoreCard()

    def _update_scorecard(self, category, points):
        """
        Assigning points to a specific category on a scorecard.

        Parameters:
        category (str): category to assign points to
        points (int): number of points to be assigned

        Returns:
        str: error message in case of a problem, None otherwise
        """
        categories = self._scorecards[self._current].categories

        if category not in categories: return 'no such category'
        if categories[category] != None: return 'category was already used'

        categories[category] = points
        self._check_game_over()

        if self._gameover:
            self._current = []
            self._build_ranking()
        else:
            self._rotate_players()

        return None

    def move(self, args, player_id): # override
        """
        Handling a player's move.

        The type of move is determined and then passed to the corresponding function.

        Parameters:
        args (dict): the current player's move
        player_id (int): player ID

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

    def _roll_dice(self, dice=list(range(0, 5))):
        """
        Rolling all or just a selection of dice.

        Parameters:
        dice (int list): list of up to five dice (0..4) to be rolled

        Returns:
        str: error message in case the move was illegal, None otherwise
        """
        if self._dice_rolls >= 3: return 'dice were rolled three times already'
        if len(dice) == 0: return 'no selection of dice entered'

        for d in dice:
            if d not in [0, 1, 2, 3, 4]:
                return 'invalid selection of dice'

        for d in dice:
            self._dice[d] = random.choice([1, 2, 3, 4, 5, 6])

        self._dice_rolls += 1

        return None

    def _add_points(self, category):
        """
        The current combination of dice is evaluated according to the category and to the rules of the game. The calculated points are then added to the specified category on the scorecard.

        Parameters:
        category (str): the chosen category

        Returns:
        str: error message in case the move was illegal, None otherwise
        """
        if category in self._upper_section:
            # calculate sum of dice with the same value according to the category:
            face_value = self._upper_section.index(category) + 1
            count = self._dice.count(face_value)
            if count == 0: return f'there are no {face_value}s'
            points = count * face_value

            return self._update_scorecard(category, points)
        else:
            # NOTE implement lower section of Yahtzee scorecard here
            return 'not implemented'

    def _cross_out(self, category):
        """
        Crossing out a category by adding zero points to it.

        Parameters:
        category (str): category to be crossed out

        Returns:
        str: error message in case the move was illegal, None otherwise
        """
        return self._update_scorecard(category, 0)

    def _set_name(self, name, player_id):
        """
        Add the submitted player name to the scorecard.

        Parameters:
        name (str): submitted name
        player_id (int): player ID

        Returns:
        str: error message in case of a problem, None otherwise
        """
        if not name:
            return 'name must not be empty'

        if self._scorecards[player_id].player_name:
            return 'you cannot change your name'

        for sc in self._scorecards.values():
            if sc.player_name == name:
                return 'name already in use'

        self._scorecards[player_id].player_name = name
        self._current.remove(player_id)

        if not self._current:
            self._current = random.randint(0, self._players - 1)

        return None

    def state(self, player_id): # override
        """
        Returns the game state as a dictionary.

        Parameters:
        player_id (int): player ID

        Returns:
        dict: game state
        """
        state = {'scorecard':self._scorecards[player_id].categories}

        if type(self._current) != list:
            current_name = self._scorecards[self._current].player_name
            if current_name:
                state['current_name'] = current_name

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

    def _rotate_players(self):
        self._dice_rolls = 0
        self._roll_dice()
        self._current = (self._current + 1) % self._players

    def game_over(self): # override
        return self._gameover

    def _check_game_over(self):
        """
        Game is over as soon as all categories on all scorecards are filled.
        """
        over = True

        for sc in self._scorecards.values():
            if not sc.full():
                over = False
                break

        self._gameover = over

    def _build_ranking(self):
        """
        Build a dictionary mapping names to points.
        """
        for sc in self._scorecards.values():
            self._ranking[sc.player_name] = sc.total_points()

    @staticmethod
    def min_players(): # override
        return 1

    @staticmethod
    def max_players(): # override
        return 8
