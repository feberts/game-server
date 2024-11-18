#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client. If you want to test it on a single machine, just run this program twice in separate shells.
"""

from game_server_api import GameServerAPI
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

game = GameServerAPI()

# join game:
my_id, err = game.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame')

if err: # no game started yet
    # start new game:
    my_id, err = game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2)
    if err: fatal(err)

state, err = game.state()
if err: fatal(err)
old_state = None

while not state['gameover']:
    if state != old_state: print_board(state['board'])

    if my_id in state['current']: # my turn
        while True:
            pos = user_input(f'\nYour ({symbols[my_id]}) turn: ')
            err = game.move(position=pos)
            if err: print(err)
            else: break
    else:
        if state != old_state: print("Opponent's turn ...")
        time.sleep(0.5)

    old_state = state
    state, err = game.state()
    if err: fatal(err)

print_board(state['board'])
winner = state['winner']

if winner == None:
    print('No winner...')
elif winner == my_id:
    print(f'You ({symbols[my_id]}) win!')
else:
    print(f'You ({symbols[my_id]}) lose...')
