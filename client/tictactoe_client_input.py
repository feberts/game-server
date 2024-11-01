#!/usr/bin/env python3
"""
Tic-tac-toe input client.

This program joins a game as an active player and submits moves. It must be used in combination with the output client. The output client connects to a game session as a passive observer. This way, the implementation of input and output can be divided between two programs. Both programs need to pass the same value for the name parameter when connecting to a game session.
"""

from game_server_api import GameServerAPI
import time

def user_input():
    while True:
        try:
            return int(input('Input: '))
        except KeyboardInterrupt:
            exit()
        except:
            print('Integers only!')

def fatal(msg):
    print(msg)
    exit()

game = GameServerAPI()

# join game:
my_id, err = game.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', name='bob')

if err: # no game started yet
    # start new game:
    my_id, err = game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2, name='bob')
    if err: fatal(err)

state, err = game.state()
if err: fatal(err)

while True:
    pos = user_input()
    err = game.move(position=pos)
    if err: print(err)

    state, err = game.state()
    if err: fatal(err)
    if state['gameover']: break

print('End')
