"""
Echo!

Not really a game, but occasionally useful for debugging and testing.
"""

from abstract_game import AbstractGame

class Echo(AbstractGame):
    """
    An unmodified copy of the data received is sent back to the client. The game
    is over as soon as the message 'quit' is received.
    """

    def __init__(self, players):
        self._message = ''
        self._gameover = False

    @staticmethod
    def min_players():
        return 1

    @staticmethod
    def max_players():
        return 1

    def current_player(self):
        return [0]

    def move(self, args, player_id):
        if 'msg' not in args:
            return "keyword argument 'msg' missing"
        self._message = args['msg']
        if self._message == 'quit':
            self._gameover = True
        return None

    def game_over(self):
        return self._gameover

    def state(self, player_id):
        return {'echo': self._message}
