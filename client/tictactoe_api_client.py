#!/usr/bin/env python3
"""
Tic-tac-toe API client.

This client program demonstrates the use of a wrapper API for tic-tac-toe. Implementing wrapper functions is not necessary because the game server API is generic and works with every game, but it can simplify the API usage.
"""

from tictactoe_api import TicTacToeAPI
import time

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
            exit()
        except:
            print('Integers only!')

def fatal(msg):
    print(msg)
    exit()

game = TicTacToeAPI()

# join game:
my_id, err = game.join_game(token='mygame', name='herbert')

if err: # no game started yet
    # start new game:
    my_id, err = game.start_game(token='mygame')
    if err: fatal(err)

state, err = game.state()
if err: fatal(err)
old_state = None

while not state.gameover:
    if state != old_state: print_board(state.board)

    if state.current == my_id: # my turn
        while True:
            pos = user_input(f'\nYour ({symbols[my_id]}) turn: ')
            err = game.move(pos)
            if err: print(err)
            else: break
    else:
        if state != old_state: print("Opponent's turn ...")
        time.sleep(0.5)

    old_state = state
    state, err = game.state()
    if err: fatal(err)

print_board(state.board)
winner = state.winner

if winner == None:
    print('No winner...')
elif winner == my_id:
    print(f'You ({symbols[my_id]}) win!')
else:
    print(f'You ({symbols[my_id]}) lose...')
