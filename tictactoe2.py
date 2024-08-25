#!/usr/bin/env python3

# object oriented version; class Game acts as a pseudo server

class State:
    board = [-1] * 9
    current = 0
    gameover = False
    winner = None

class Game:
    __state = State()

    def start(self):
        return 0 # player id

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
        for i, j, k in ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)):
            if self.__state.board[i] == self.__state.board[j] == self.__state.board[k] == self.__state.current:
                self.__state.winner = self.__state.current
                self.__state.gameover = True
                
    def __check_gameover(self):
        if -1 not in self.__state.board:
            self.__state.gameover = True
    
    def opponent_move(self):
        """makeshift method to simulate an opponents move"""
        self.move(self.__state.board.index(-1))


        


players = ('x', 'o')

def print_board(board):
    board = [i if board[i] == -1 else players[board[i]] for i in range(9)]
    print(f' {board[0]} | {board[1]} | {board[2]}', f'---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', f'---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def user_input(current):
    while True:
        try:
            return int(input(f'Your turn {players[current]}: '))
        except KeyboardInterrupt:
            exit()
        except:
            print('Integers only!')

import time

game = Game()
my_id = game.start()
state = game.state()

while not state.gameover:
    print_board(state.board)

    if state.current == my_id: # my turn
        while True:
            pos = user_input(state.current)
            ok = game.move(pos)
            if ok:
                break
            else:
                print('Illegal move!')
    else:
        print(f'Opponents turn {players[state.current]} ...')
        time.sleep(1)
        game.opponent_move() # trigger opponents move

    state = game.state()
    
print_board(state.board)

if state.winner == None:
    print('No winner!')
else:
    print(f'Player {players[state.winner]} wins!')

#15368
