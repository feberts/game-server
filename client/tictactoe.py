#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client. TODO
"""

from game_server_api import GameServerAPI

api = GameServerAPI()

player_id, msg = api.start_game(server='127.0.0.1', port=4711, game='TicTacToe', players=2, token='mygame')

#print('ID:', player_id, '\nError message:', msg)
