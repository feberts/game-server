"""
Tic-tac-toe API wrapper.

This is a demonstration of how one could implement an API with wrapper functions for a specific game. Doing this is not necessary, because the game server API is generic and works with every game, but it can simplify the API usage.
"""

import game_server_api

class TicTacToeAPI:
    """
    Class TicTacToeAPI.

    This class provides API wrapper functions for tic-tac-toe.
    """

    def __init__(self):
        self._api = game_server_api.GameServerAPI()

    def start_game(self, token, name=''):
        return self._api.start_game('127.0.0.1', 4711, 'TicTacToe', token, 2, name)

    def join_game(self, token, name=''):
        return self._api.join_game('127.0.0.1', 4711, 'TicTacToe', token, name)

    def move(self, position):
        return self._api.move(position=position)

    def state(self, blocking=True):
        state, err = self._api.state(blocking)
        if err: return None, err
        return State(state['board'], state['current'][0], state['gameover'], state['winner']), None

    def watch(self, token, name):
        return self._api.watch('127.0.0.1', 4711, 'TicTacToe', token, name)

class State:
    """
    Class State.

    Usually, a dictionary is returned by the state function. Here, all data is encapsulated in a class for easy access.
    """

    def __init__(self, board, current, gameover, winner):
        self.board = board
        self.current = current
        self.gameover = gameover
        self.winner = winner
