#!/usr/bin/env python3
"""
Tic-tac-toe random player.

This client joins a game and submits random (but legal) moves. It is used in combination with the learning client to produce data for AI training.
"""

from game_server_api import GameServerAPI
import random

def fatal(msg):
    print(msg)
    exit()

def random_move(board):
    vacant = [i for i in range(9) if board[i] == -1]
    return random.choice(vacant)

game = GameServerAPI()
my_id, err = game.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='learn')
if err: fatal(err)
    
while True:
    state, err = game.state()
    if err: fatal(err)

    if my_id in state['current'] and not state['gameover']:
        pos = random_move(state['board'])
        err = game.move(position=pos)
        if err: fatal(err)
