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
        self.my_id = None

    def start_game(self, token, players=1, name=''):
        self.my_id, err = self._api.start_game('127.0.0.1', 4711, 'Yahtzee', token, players, name)
        return self.my_id, err

    def join_game(self, token, name=''):
        self.my_id, err = self._api.join_game('127.0.0.1', 4711, 'Yahtzee', token, name)
        return self.my_id, err

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
        return State(state, self.my_id), None

    def watch(self, token, name):
        return self._api.watch('127.0.0.1', 4711, 'Yahtzee', token, name)

class State:
    """
    Class State.

    Usually, a dictionary is returned by the state function. Here, all data is encapsulated in a class for easy access.
    """

    def __init__(self, state, my_id):
        gameover = state['gameover']
        self.my_turn = my_id in state['current']
        self.gameover = gameover
        self.scorecard = state['scorecard']
        self.dice = state['dice'] if gameover == False else None
        self.current_name = state['current_name'] if 'current_name' in state else None
        self.ranking = state['ranking'] if gameover == True else None
