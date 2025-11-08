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

    def start_game(self):
        return self._api.start_game(2)

    def join_game(self):
        return self._api.join_game()

    def move(self, position):
        return self._api.move(position=position)

    def state(self):
        state, err = self._api.state()
        if err: return None, err
        return State(state['board'], state['current'][0], state['gameover'], state['winner']), None

class State:
    """
    Class State.

    Usually, a dictionary is returned by the state function. Here, all data is
    encapsulated in a class for easy access.
    """

    def __init__(self, board, current, gameover, winner):
        self.board = board
        self.current = current
        self.gameover = gameover
        self.winner = winner
