# this module implements a tic-tac-toe game class used by the server

import abstract_game

class State(abstract_game.AbstractGame):
    board = []
    current = 0
    gameover = False
    winner = None
    def __init__(self):
        self.board = [-1] * 9

class Game:
    __state = State()

    def state(self):
        return self.__state

    def move(self, pos):
        if self.__move_valid(pos):
            self.__update_board(pos)
            self.__check_win()
            self.__check_gameover()
            self.__state.current ^= 1 # rotate players
            return True
        return False

    def __move_valid(self, pos):
        try:
            return pos >= 0 and self.__state.board[pos] == -1
        except:
            return False

    def __update_board(self, pos):
        self.__state.board[pos] = self.__state.current

    def __check_win(self):
        b = self.__state.board
        for i, j, k in ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)):
            if b[i] == b[j] == b[k] == self.__state.current:
                self.__state.winner = self.__state.current
                self.__state.gameover = True

    def __check_gameover(self):
        if -1 not in self.__state.board:
            self.__state.gameover = True
