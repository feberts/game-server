#!/usr/bin/env python3
"""
Tic-tac-toe learner.

This client learns how to play tic-tac-toe. It collects data for reinforcement learning by performing random moves against another client and uses a method designed by Donald Michie in 1961 to develop a strategy. During training, a statistic is printed showing how the winning rate increases with more training.

Article by Donald Michie describing his method:
https://academic.oup.com/comjnl/article/6/3/232/360077

Wikipedia article on his method:
https://en.wikipedia.org/w/index.php?title=Matchbox_Educable_Noughts_and_Crosses_Engine&oldid=1242708397
"""

from game_server_api import GameServerAPI
import time
import random

def fatal(msg):
    print(msg)
    exit()

def random_move(board):
    vacant = [i for i in range(9) if board[i] == -1]
    return random.choice(vacant)

game = GameServerAPI()
my_id, err = game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='learn', players=2)
if err: fatal(err)

games = 0
won = 0
lost = 0
draw = 0

time_start = time.time()

while games < 1000:
    state, err = game.state()
    if err: fatal(err)

    while not state['gameover']:
        if state['current'] == my_id:
            pos = random_move(state['board'])
            err = game.move(position=pos)
            if err: fatal(err)

        state, err = game.state()
        if err: fatal(err)

    winner = state['winner']
    
    games += 1

    if winner == None:
        draw += 1
    elif winner == my_id:
        won += 1
    else:
        lost += 1
        
    game.reset_game()

print(f'games: {games}, won: {won}, lost: {lost}, draw: {draw}, win rate: {won / games}, win rate opponent: {lost / games}')

print(time.time() - time_start, 'seconds')
