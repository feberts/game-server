#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client.
"""

import threading
import time

from game_server_api import GameServerAPI

def client_start():
    api = GameServerAPI()

    my_id, err = api.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2)

    if err:
        print(err)
        exit()

    print('Player ID:', my_id)

def client_join():
    time.sleep(0.1)
    api = GameServerAPI()

    my_id, err = api.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame')

    if err:
        print(err)
        exit()

    print('Player ID:', my_id)


threading.Thread(target=client_start, args=(), daemon=True).start()

for _ in range(4):
    threading.Thread(target=client_join, args=(), daemon=True).start()

time.sleep(5)
