#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client.
"""

from game_server_api import GameServerAPI

api = GameServerAPI()

my_id, err = api.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2)

#my_id, err = api.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame2', players=2) # TODO del

if err:
    print(err)
    exit()

print('Player ID:', my_id)
