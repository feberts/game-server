#!/usr/bin/env python3
"""
Tic-tac-toe input client.

This program joins a game as an active player and submits moves. It must be used
in combination with the output client. The output client connects to a game
session as a passive observer. This way, the implementation of input and output
can be divided between two programs. Both programs need to pass the same value
for the name parameter when connecting to a game session.
"""

from game_server_api import GameServerAPI, GameError

game = GameServerAPI(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2, name='bob')

def user_input(prompt):
    while True:
        try:
            return int(input(prompt)) - 1
        except KeyboardInterrupt:
            print('')
            exit()
        except ValueError:
            print('Integers only!')

my_id = game.join()

while True:
    pos = user_input('Input: ')

    try:
        game.move(position=pos)
    except GameError as e:
        print(e)

    state = game.state()
    if state['gameover']: break
