#!/usr/bin/env python3
"""
Tic-tac-toe learner.

This client learns how to play tic-tac-toe. It uses a method designed by British researcher Donald Michie in 1961 to develop a strategy. During training, a statistic is printed showing how the performance improves over time.

Article by Donald Michie describing his method: https://academic.oup.com/comjnl/article/6/3/232/360077

Wikipedia article on his method: https://en.wikipedia.org/w/index.php?title=Matchbox_Educable_Noughts_and_Crosses_Engine&oldid=1242708397
"""

import random
import time

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
start = time.time()

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

# print('Time:', time.time() - start)
