#!/usr/bin/env python3
"""
Test bench for client server interaction in separate threads. (This program has no specific purpose.)
"""

import threading
import time

from game_server_api import GameServerAPI

server = '127.0.0.1'
port = 4711
game = 'TicTacToe'
token = 'mygame2'
players = 2

def client_start():
    api = GameServerAPI()
    my_id, err = api.start_game(server=server, port=port, game=game, token=token, players=players, name='Bob')

    if err:
        print(err)
        exit()

    print('Player ID Bob:', my_id)

def client_join():
    api = GameServerAPI()
    my_id, err = api.join_game(server=server, port=port, game=game, token=token, name='Alice')

    if err:
        print(err)
        exit()

    print('Player ID Alice:', my_id)

def client_watch():
    api = GameServerAPI()
    my_id, err = api.watch(server=server, port=port, game=game, token=token, name='Alice')

    if err:
        print(err)
        exit()

    print('Observed ID:', my_id)

threading.Thread(target=client_start, args=(), daemon=True).start()
time.sleep(0.1)
threading.Thread(target=client_join, args=(), daemon=True).start()
time.sleep(0.1)
threading.Thread(target=client_watch, args=(), daemon=True).start()

#for _ in range(players):
    #threading.Thread(target=client_join, args=(), daemon=True).start()

time.sleep(1)
