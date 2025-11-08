#!/usr/bin/env python3
"""
Tic-tac-toe client using the API wrapper.

This client program demonstrates the use of an API wrapper for tic-tac-toe.
Implementing wrapper functions is not necessary because the game server API is
generic and works with every game, but it can simplify the API usage.
"""

from tictactoe_api import TicTacToeAPI

symbols = ('x', 'o')

def print_board(board):
    print('\n' * 100)
    board = [i if board[i] == -1 else symbols[board[i]] for i in range(9)]
    print(f' {board[0]} | {board[1]} | {board[2]}', '---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', '---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def user_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except KeyboardInterrupt:
            print('')
            exit()
        except ValueError:
            print('Integers only!')

def fatal(msg):
    print(msg)
    exit()

game = TicTacToeAPI(token='mygame')

my_id, err = game.join_game()

if err: # no game started yet
    my_id, err = game.start_game()
    if err: fatal(err)

state, err = game.state()
if err: fatal(err)

while not state.gameover:
    print_board(state.board)

    if state.current == my_id: # my turn
        while True:
            pos = user_input(f'\nYour ({symbols[my_id]}) turn: ')
            err = game.move(pos)
            if err: print(err)
            else: break
    else:
        print("Opponent's turn ...")

    state, err = game.state()
    if err: fatal(err)

print_board(state.board)
winner = state.winner

if winner is None:
    print('No winner...')
elif winner == my_id:
    print(f'You ({symbols[my_id]}) win!')
else:
    print(f'You ({symbols[my_id]}) lose...')
