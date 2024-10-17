#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client.
"""

from game_server_api import GameServerAPI

api = GameServerAPI()

api.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2)
