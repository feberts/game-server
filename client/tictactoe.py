#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client.
"""

from game_server_api import GameServerAPI
import threading
import time

def client_1():
    api = GameServerAPI()

    my_id, err = api.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2)

    if err:
        print(err)
        exit()

    print('Player ID:', my_id)

def client_2():
    api = GameServerAPI()

    my_id, err = api.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame')

    if err:
        print(err)
        exit()

    print('Player ID:', my_id)


t1 = threading.Thread(target=client_1, args=(), daemon=False)
t2 = threading.Thread(target=client_2, args=(), daemon=False)

t1.start()
time.sleep(0.5)
t2.start()

#t1.join()
#t2.join()

