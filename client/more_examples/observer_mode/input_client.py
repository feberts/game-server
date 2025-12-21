#!/usr/bin/env python3
"""
Tic-tac-toe input client.

This program joins a game as an active player and submits moves. It must be used
in combination with the output client. The output client connects to a game
session as a passive observer. This way, the implementation of input and output
can be divided between two programs. Both programs need to pass the same value
for the name parameter when connecting to a game session.
"""

from game_server_api import GameServerAPI

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

def fatal(msg):
    print(msg)
    exit()

my_id, err = game.join()
if err: fatal(err)

while True:
    pos = user_input('Input: ')
    err = game.move(position=pos)
    if err: print(err)

    state, err = game.state()
    if err: fatal(err)
    if state['gameover']: break
