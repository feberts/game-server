#!/usr/bin/env python3

# object oriented version; class Game acts as a pseudo server

from tictactoe import TicTacToe
#import time

game = TicTacToe(2)

"""
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
        time.sleep(2)
        game.opponent_move() # trigger opponents move

    state = game.state()

print_board(state.board)

if state.winner == None:
    print('No winner!')
else:
    print(f'Player {players[state.winner]} wins!')
"""
