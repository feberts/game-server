#!/usr/bin/env python3
"""
Tic-tac-toe opponent.

This client can be used in combination with the learner. It joins the game and
uses the same learning method.
"""

from game_server_api import GameServerAPI
from menace import MENACE

def fatal(msg):
    print(msg)
    exit()

game = GameServerAPI()
my_id, err = game.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='training')
if err: fatal(err)

menace = MENACE()

while True:
    # play a single game:
    state, err = game.state()
    if err: fatal(err)

    while not state['gameover']:
        if my_id in state['current']:
            pos = menace.move(state['board'])
            err = game.move(position=pos)
            if err: fatal(err)

        state, err = game.state()
        if err: fatal(err)

    # let menace know about the outcome:
    winner = state['winner']
    if winner == my_id:
        menace.win()
    elif winner is None:
        menace.draw()
    else:
        menace.loss()
