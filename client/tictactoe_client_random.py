#!/usr/bin/env python3
"""
Tic-tac-toe client.TODO

This program connects to the game server to play tic-tac-toe against another client. If you want to test it on a single machine, just run this program twice in separate shells.TODO
"""

# TODO prüfen ob weglassen der fehlernbehandlung zu besserer performanz führt

from game_server_api import GameServerAPI
import random
import time

def random_move(board):
    vacant = [i for i in range(9) if board[i] == -1]
    return random.choice(vacant)

def fatal(msg):
    print(msg)
    exit()

game = GameServerAPI()
my_id, err = game.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='learn') # TODO token ändern
if err: fatal(err)
    
while True:

    state, err = game.state()
    if err: fatal(err)

    if state['current'] == my_id and not state['gameover']: # my turn
        pos = random_move(state['board'])
        err = game.move(position=pos)
        if err: print(err)

    time.sleep(0.1) # TODO rm
