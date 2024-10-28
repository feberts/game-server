#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client.
"""

from game_server_api import GameServerAPI

def print_board(board):
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
my_id, err = api.start_game(server='127.0.0.1', port=4711, game=game, token=token, players=players)

current = game.current_player()
state = game.state()

while not state['gameover']:
    print_board(state['board'])

    while True:
        pos = user_input(current)
        err = game.move({'position':pos})
        if err:
            print(err)
        else:
            break

    state = game.state()
    current = game.current_player()

print_board(state['board'])
winner = state['winner']

if winner == None:
    print('No winner!')
else:
    print(f'Player {players[int(winner)]} wins!')

"""


import threading
import time

from game_server_api import GameServerAPI

game = 'TicTacToe'
token = 'mygame'
players = 2

def client_start():
    api = GameServerAPI()
    my_id, err = api.start_game(server='127.0.0.1', port=4711, game=game, token=token, players=players)

    if err:
        print(err)
        exit()

    print('Player ID:', my_id)

    err = api.move(position=7)
    if err: print(err)
    
    time.sleep(0.5)

    state, err = api.state()
    if err:
        print(err)
    else:
        print(state)
    
    time.sleep(0.5)

    err = api.move(position=8)
    if err: print(err)


def client_join():
    api = GameServerAPI()
    my_id, err = api.join_game(server='127.0.0.1', port=4711, game=game, token=token)

    if err:
        print(err)
        exit()

    print(f'Player ID:', my_id)

threading.Thread(target=client_start, args=(), daemon=True).start()

time.sleep(0.5)

for _ in range(1):
    threading.Thread(target=client_join, args=(), daemon=True).start()

time.sleep(5)
"""
