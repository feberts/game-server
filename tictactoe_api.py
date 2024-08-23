#!/usr/bin/env python3

class State():
    board = [-1] * 9
    current = 0
    gameover = False
    winner = None

class Game:
    __state = State()

    def state(this):
        return this.__state

    def __update_board(this, pos):
        this.__state.board[pos] = this.__state.current

    def move(this, pos):
        if this.__move_valid(pos):
            this.__update_board(pos)
            this.__check_win()
            this.__state.current ^= 1
            return True
        return False
    
    def __check_win(this):
        for i, j, k in ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)):
            if this.__state.board[i] == this.__state.board[j] == this.__state.board[k] == this.__state.current:
                this.__state.winner = this.__state.current
                this.__state.gameover = True
                
    def __move_valid(this, pos):
        try:
            return pos >= 0 and this.__state.board[pos] == -1
        except:
            return False


players = ('x', 'o')
me = 0

def print_board(board):
    board = [i if board[i] == -1 else players[board[i]] for i in range(9)]
    print(f' {board[0]} | {board[1]} | {board[2]}', f'---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', f'---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def user_input(current):
    while True:
        try:
            return int(input(f'Player {players[current]}: '))
        except KeyboardInterrupt:
            exit()
        except:
            print('Integers only!')

game = Game()
state = game.state()

while not state.gameover:
    print_board(state.board)
    if state.current == me:
        pos = user_input(state.current)
        ok = game.move(pos)
        if not ok:
            print('Illegal move!')
        else
            
    state = game.state()




