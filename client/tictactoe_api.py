"""
Tic-tac-toe API.

TODO
"""

import game_server_api

class State:
    def __init__(self, board, current, gameover, winner):
        self.board = board
        self.current = current
        self.gameover = gameover
        self.winner = winner

class TicTacToeAPI(game_server_api.GameServerAPI):
    """
    TODO
    """
    def start_game(self, token, name=''):
        return super().start_game('127.0.0.1', 4711, 'TicTacToe', token, 2, name)

    def join_game(self, token, name=''):
        return super().join_game('127.0.0.1', 4711, 'TicTacToe', token, name)

    def move(self, position):
        return super().move(position=position)

    def state(self):
        state, err = super().state()
        if err: return None, err
        return State(state['board'], state['current'], state['gameover'], state['winner']), None

    def watch(self, token, name):
        return super().watch('127.0.0.1', 4711, 'TicTacToe', token, name)
