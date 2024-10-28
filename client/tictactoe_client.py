#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client.
"""

# TODO implement tic-tac-toe client


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
    
    err = api.move(position=42, string='hallo', liste=[1,2,3])

    if err:
        print(err)

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
