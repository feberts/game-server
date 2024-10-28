#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client.
"""

import time
from game_server_api import GameServerAPI

def print_board(board):
    print('\n' * 100)
    board = [i if board[i] == -1 else players[board[i]] for i in range(9)]
    print(f' {board[0]} | {board[1]} | {board[2]}', '---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', '---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def user_input(current):
    while True:
        try:
            return int(input(f'Your turn {players[current]}: '))
        except KeyboardInterrupt:
            exit()
        except:
            print('Integers only!')

players = ('x', 'o')

game = GameServerAPI()

my_id, err = game.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame')

if err: my_id, err = game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2)

state, err = game.state() # TODO err prüfen
current = state['current']

while not state['gameover']:
    print_board(state['board'])

    if current == my_id: # my turn
        while True:
            pos = user_input(current)
            err = game.move(position=pos)
            if err:
                print(err)
            else:
                break
    else:
        print('Opponents turn ...')
        time.sleep(1)

    state, err = game.state() # TODO err prüfen
    current = state['current']

print_board(state['board'])
winner = state['winner']

if winner == None:
    print('No winner!')
elif winner == my_id:
    print(f'You ({players[my_id]}) won!')
else:
    print(f'You ({players[my_id]}) lost...')
