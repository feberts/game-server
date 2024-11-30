#!/usr/bin/env python3
"""
Tic-tac-toe observer client.

This program connects to a game session as a passive observer. It can be used in combination with the input client. The input client joins a game as an active player and submits moves. This way, the implementation of input and output can be divided between two programs. Both programs need to pass the same value for the name parameter when connecting to a game session.
"""

import time

from game_server_api import GameServerAPI

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

state, err = game.state(blocking=False)
if err: fatal(err)

while not state['gameover']:
    print_board(state['board'])

    if observed_id in state['current']: # my turn
        print(f'Your ({symbols[observed_id]}) turn')
    else:
        print("Opponent's turn ...")

    state, err = game.state() # TODO blockiert nicht, wenn der beobachtete Spieler an der Reihe ist
    if err: fatal(err)

print_board(state['board'])
winner = state['winner']

if winner == None:
    print('No winner...')
elif winner == observed_id:
    print(f'You ({symbols[observed_id]}) win!')
else:
    print(f'You ({symbols[observed_id]}) lose...')
