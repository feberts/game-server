"""
Tic-tac-toe game.

This module implements a tic-tac-toe game class.
"""

from abstract_game import AbstractGame

class TicTacToe(AbstractGame):
    """
    Class TicTacToe.
    
    This class implements a tic-tac-toe game.
    """
    def __init__(self, players): # override
        """
        Constructor.

        Parameters:
        players (int): number of players (unused)
        """
        pass

    class State:
        board = [-1] * 9
        current = 0
        gameover = False
        winner = None

    _state = State()

    def state(self, player_id): # override
        """
        Returns the game state as a dictionary.

        Dictionary keys and values:
        'board'    : integer list of size 9, values: -1 = empty; 0 or 1 = player
        'gameover' : True if game has ended, else False
        'winner'   : player ID, or None if there is no winner

        Parameters:
        player_id (int): player ID (unused)

        Returns:
        dict: game state
        """
        return {'board':self._state.board, 'gameover':self._state.gameover, 'winner':self._state.winner}

    def current_player(self): # override
        """
        Returns the current player's ID.

        Returns:
        int: current player's ID
        """
        return self._state.current

    def move(self, move): # override
        """
        Submit a move.

        The move is passed as a dictionary containing the key 'position' with a board position (0-8) as its value.

        Parameters:
        move (dict): the current player's move

        Returns:
        tuple(bool, str):
            bool: to inform the client whether the move was valid or not
            str: error message in case the move was illegal, an empty string otherwise
        """
        # TODO param checks
        pos = int(move['position'])
        if self._move_valid(pos):
            self._update_board(pos)
            self._check_win()
            self._check_gameover()
            self._state.current ^= 1 # rotate players
            return True, ''
        return False, 'position already occupied'

    def _move_valid(self, pos):
        try:
            return pos >= 0 and self._state.board[pos] == -1
        except:
            return False

    def _update_board(self, pos):
        self._state.board[pos] = self._state.current

    def _check_win(self):
        b = self._state.board
        for i, j, k in ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)):
            if b[i] == b[j] == b[k] == self._state.current:
                self._state.winner = self._state.current
                self._state.gameover = True

    def _check_gameover(self):
        if -1 not in self._state.board:
            self._state.gameover = True

    def min_players(self): # override
        return 2

    def max_players(self): # override
        return 2
