#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client.
"""

from game_server_api import GameServerAPI

api = GameServerAPI()

player_id, msg = api.start_game(server='127.0.0.1', port=4711, game='TicTacToe', players=2, token='mygame')

#player_id, msg = api.start_game(server='127.0.0.11', port=4711, game='TicTacToe', players=2, token='mygame')
#player_id, msg = api.start_game(server='127.0.0.256', port=4711, game='TicTacToe', players=2, token='mygame')
#player_id, msg = api.start_game(server='sdfgh', port=4711, game='TicTacToe', players=2, token='mygame')
#player_id, msg = api.start_game(server='', port=4711, game='TicTacToe', players=2, token='mygame')
#player_id, msg = api.start_game(server=34, port=4711, game='TicTacToe', players=2, token='mygame')
#player_id, msg = api.start_game(server='', port=4712, game='TicTacToe', players=2, token='mygame')


#player_id, msg = api.start_game(server='127.0.0.1', port=4712, game='TicTacToe', players=2, token='mygame')
#player_id, msg = api.start_game(server='127.0.0.1', port=471159875, game='TicTacToe', players=2, token='mygame')
#player_id, msg = api.start_game(server='127.0.0.1', port="4711", game='TicTacToe', players=2, token='mygame')
#player_id, msg = api.start_game(server='127.0.0.1', port=-4711, game='TicTacToe', players=2, token='mygame')


#player_id, msg = api.start_game(server='127.0.0.1', port=4711, game='', players=2, token='mygame')
#player_id, msg = api.start_game(server='127.0.0.1', port=4711, game=456, players=2, token='mygame')


#player_id, msg = api.start_game(server='127.0.0.1', port=4711, game='TicTacToe', players=0, token='mygame')
#player_id, msg = api.start_game(server='127.0.0.1', port=4711, game='TicTacToe', players="2", token='mygame')


#player_id, msg = api.start_game(server='127.0.0.1', port=4711, game='TicTacToe', players=2, token='')
#player_id, msg = api.start_game(server='127.0.0.1', port=4711, game='TicTacToe', players=2, token=8765)

if not player_id:
    print(msg)
    print('end')
    exit()

print('Player ID:', player_id)
