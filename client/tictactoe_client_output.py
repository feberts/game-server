#!/usr/bin/env python3
"""
Tic-tac-toe observer client.TODO

This program starts a tic-tac-toe client in observation mode.TODO
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

def fatal(msg):
    print(msg)
    exit()

game = GameServerAPI()

# observe game:
observed_id, err = game.watch(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', name='bob')
if err: fatal(err)

state, err = game.state()
if err: fatal(err)

while not state['gameover']:
    print_board(state['board'])

    if state['current'] == observed_id: # my turn
        print(f'Your ({symbols[observed_id]}) turn')
    else:
        print("Opponent's turn ...")

    state, err = game.state()
    if err: fatal(err)
    time.sleep(0.5)

print_board(state['board'])
winner = state['winner']

if winner == None:
    print('No winner...')
elif winner == observed_id:
    print(f'You ({symbols[observed_id]}) win!')
else:
    print(f'You ({symbols[observed_id]}) lose...')
