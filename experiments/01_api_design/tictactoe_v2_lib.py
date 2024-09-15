# this module implements class Game to imitate a game server

class State:
    board = [-1] * 9
    current = 0
    gameover = False
    winner = None

class Game:
    _state = State()

    def start(self):
        return 0 # player id

    def state(self):
        return self._state

    def move(self, pos):
        if self._move_valid(pos):
            self._update_board(pos)
            self._check_win()
            self._check_gameover()
            self._state.current ^= 1 # rotate players
            return True
        return False

    def _move_valid(self, pos):
        try:
            return pos >= 0 and self._state.board[pos] == -1
        except:
            return False

    def _update_board(self, pos):
        self._state.board[pos] = self._state.current

    def _check_win(self):
        for i, j, k in ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)):
            if self._state.board[i] == self._state.board[j] == self._state.board[k] == self._state.current:
                self._state.winner = self._state.current
                self._state.gameover = True

    def _check_gameover(self):
        if -1 not in self._state.board:
            self._state.gameover = True

    def opponent_move(self):
        """makeshift method to simulate an opponents move"""
        self.move(self._state.board.index(-1))
