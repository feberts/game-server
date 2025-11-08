"""
Tic-tac-toe API wrapper.

This is a demonstration of how one could implement an API with wrapper functions
for a specific game. Doing this is not necessary, because the game server API is
generic and works with every game, but it can simplify the API usage.
"""

import game_server_api

class TicTacToeAPI:
    """
    Class TicTacToeAPI.

    This class provides API wrapper functions for tic-tac-toe.
    """

    def __init__(self, token, name=''):
        self._api = game_server_api.GameServerAPI('127.0.0.1', 4711, 'TicTacToe', token, name)
        self.my_id = None

    def start_game(self):
        self.my_id, err = self._api.start_game(2)
        return self.my_id, err

    def join_game(self):
        self.my_id, err = self._api.join_game()
        return self.my_id, err

    def put_mark(self, position):
        return self._api.move(position=position)

    def state(self):
        state, err = self._api.state()
        if err: return None, err
        return State(state, self.my_id), None

class State:
    """
    Class State.

    Usually, a dictionary is returned by the state function. Here, all data is
    encapsulated in a class for easy access.
    """

    def __init__(self, state, my_id):
        self.my_turn = my_id in state['current']
        self.board = state['board']
        self.gameover = state['gameover']
        self.winner = None if state['winner'] is None else state['winner'] == my_id
