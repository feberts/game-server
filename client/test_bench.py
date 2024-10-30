#!/usr/bin/env python3
"""
Test bench for client server interaction in separate threads.
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

def client_join():
    api = GameServerAPI()
    my_id, err = api.join_game(server='127.0.0.1', port=4711, game=game, token=token)

    if err:
        print(err)
        exit()

    print('Player ID:', my_id)

def client_watch():
    api = GameServerAPI()
    my_id, err = api.watch(server='127.0.0.1', port=4711, game=game, token=token)

    if err:
        print(err)
        exit()

    print('Player ID:', my_id)

threading.Thread(target=client_start, args=(), daemon=True).start()
time.sleep(0.1)
threading.Thread(target=client_join, args=(), daemon=True).start()
time.sleep(0.1)
threading.Thread(target=client_watch, args=(), daemon=True).start()

#for _ in range(players):
    #threading.Thread(target=client_join, args=(), daemon=True).start()

time.sleep(2)
