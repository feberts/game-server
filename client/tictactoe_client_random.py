#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client. If you want to test it on a single machine, just run this program twice in separate shells.
"""

from game_server_api import GameServerAPI
import time
import random

symbols = ('x', 'o')

def print_board(board):
    print('\n' * 100)
    board = [i if board[i] == -1 else symbols[board[i]] for i in range(9)]
    print(f' {board[0]} | {board[1]} | {board[2]}', '---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', '---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def random_move(board):
    vacant = [i for i in range(9) if board[i] == -1]
    return random.choice(vacant)

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

while not state['gameover']:
    print_board(state['board'])

    if state['current'] == my_id: # my turn
        while True:
            pos = random_move(state['board'])
            err = game.move(position=pos)
            if err: print(err)
            else: break
    else:
        print("Opponent's turn ...")
        time.sleep(0.5)

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
