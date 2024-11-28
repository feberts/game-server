#!/usr/bin/env python3
"""
Tic-tac-toe learner.

This client learns how to play tic-tac-toe using a method designed by Donald Michie (see module menace). During training, a statistic is printed showing how the performance develops over time.
"""

import random
import time # TODO rm

from game_server_api import GameServerAPI
from menace import MENACE

batch_size = 1000 # learning progress will be printed after each batch of games
number_of_batches = 100

def fatal(msg):
    print(msg)
    exit()

game = GameServerAPI()
my_id, err = game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2)
if err: fatal(err)

menace = MENACE()
batches = 0
print('games,winrate,drawrate,sum')
start = time.time() # TODO rm

while batches < number_of_batches:
    games = 0
    win = 0
    draw = 0

    # play a batch of games:
    while games < batch_size:
        # play a single game:
        state, err = game.state()
        if err: fatal(err)

        while not state['gameover']:
            if my_id in state['current']:
                pos = menace.move(state['board'])
                err = game.move(position=pos)
                if err: fatal(err)

            state, err = game.state(blocking=True)
            if err: fatal(err)

        # let menace know about the outcome:
        winner = state['winner']

        if winner == my_id:
            menace.win()
            win += 1
        elif winner == None:
            menace.draw()
            draw += 1
        else:
            menace.loss()

        # start new game:
        game.reset_game()
        games += 1

    # print training progress for the last batch of games:
    batches += 1
    winrate = win / games
    drawrate = draw / games
    games_total = batches * batch_size

    print(f'{games_total},{winrate:.3f},{drawrate:.3f},{winrate + drawrate:.3f}')

# print('Time:', time.time() - start) # TODO rm
