"""
Tic-tac-toe game.

This module provides a tic-tac-toe implementation to be executed by the framework.
"""

from abstract_game import AbstractGame

class TicTacToe(AbstractGame):
    """
    Class TicTacToe.

    This class implements a tic-tac-toe game.
    """

    class _State:
        def __init__(self):
            self.board = [-1] * 9
            self.current = 0
            self.gameover = False
            self.winner = None

    def __init__(self, _): # override
        self._state = self._State()

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
        return {'board':self._state.board, 'gameover':self._state.gameover, 'winner':self._state.winner, 'ID':player_id} # TODO ID wieder enfernen

    def current_player(self): # override
        """
        Returns the current player's ID.

        Returns:
        int: current player's ID
        """
        return self._state.current

    def move(self, args): # override
        """
        Submit a move.

        The move is passed as a dictionary containing the key 'position' with a board position (0-8) as its value.

        Parameters:
        args (dict): the current player's move

        Returns:
        str: error message in case the move was illegal, None otherwise
        """
        if 'position' not in args:
            return "keyword argument 'position' of type int missing"
        if type(args['position']) != int:
            return "type of argument 'position' must be int"

        pos = int(args['position'])
        valid, msg = self._check_move(pos)
        if not valid: return msg

        self._update_board(pos)
        self._check_win()
        self._check_board_full()
        self._state.current ^= 1 # rotate players
        return None

    def _check_move(self, pos):
        """
        Check if a move is legal.
        """
        if pos < 0 or pos > 8:
            return False, 'value must be 0..8'
        if self._state.board[pos] != -1:
            return False, 'position already occupied'
        return True, ''

    def _update_board(self, pos):
        """
        Add current player's move to the board.
        """
        self._state.board[pos] = self._state.current

    def _check_win(self):
        """
        Check if the current player has won.
        """
        b = self._state.board
        for i, j, k in ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)):
            if b[i] == b[j] == b[k] == self._state.current:
                self._state.winner = self._state.current
                self._state.gameover = True

    def _check_board_full(self):
        """
        Check if the board is filled completely.
        """
        if -1 not in self._state.board:
            self._state.gameover = True

    def min_players(): # override
        return 2

    def max_players(): # override
        return 2
