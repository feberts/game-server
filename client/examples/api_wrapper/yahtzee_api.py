"""
Yahtzee API wrapper.

This is a demonstration of how one could implement an API with wrapper functions for a specific game. Doing this is not necessary, because the game server API is generic and works with every game, but it can simplify the API usage.
"""

import game_server_api

class YahtzeeAPI:
    """
    Class YahtzeeAPI.

    This class provides API wrapper functions for Yahtzee.
    """

    def __init__(self):
        self._api = game_server_api.GameServerAPI()

    def start_game(self, token, players=1, name=''):
        return self._api.start_game('127.0.0.1', 4711, 'Yahtzee', token, players, name)

    def join_game(self, token, name=''):
        return self._api.join_game('127.0.0.1', 4711, 'Yahtzee', token, name)

    def submit_name(self, name):
        return self._api.move(name=name)

    def roll_all_dice(self):
        return self._api.move(roll_dice=list(range(0, 5)))

    def roll_some_dice(self, dice):
        return self._api.move(roll_dice=dice)

    def add_points(self, category):
        return self._api.move(score='add points', category=category)

    def cross_out_category(self, category):
        return self._api.move(score='cross out', category=category)

    def state(self, blocking=True):
        state, err = self._api.state(blocking)
        if err: return None, err
        gameover = state['gameover']
        return State(state['current'][0] if state['current'] else None,
                     gameover, state['scorecard'],
                     state['dice'] if gameover == False else None,
                     state['current_name'] if 'current_name' in state else None,
                     state['ranking'] if gameover == True else None), None

    def watch(self, token, name):
        return self._api.watch('127.0.0.1', 4711, 'Yahtzee', token, name)

class State:
    """
    Class State.

    Usually, a dictionary is returned by the state function. Here, all data is encapsulated in a class for easy access.
    """

    def __init__(self, current, gameover, scorecard, dice, current_name, ranking):
        self.current = current
        self.gameover = gameover
        self.scorecard = scorecard
        self.dice = dice
        self.current_name = current_name
        self.ranking = ranking
