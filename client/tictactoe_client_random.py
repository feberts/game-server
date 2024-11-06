#!/usr/bin/env python3
"""
Tic-tac-toe client.TODO

This program connects to the game server to play tic-tac-toe against another client. If you want to test it on a single machine, just run this program twice in separate shells.TODO
"""

from game_server_api import GameServerAPI
import time
import random

symbols = ('x', 'o')

def print_board(board):
    print('\n' * 100)
    board = [i if board[i] == -1 else symbols[board[i]] for i in range(9)]
    print(f' {board[0]} | {board[1]} | {board[2]}', '---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', '---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def random_move(board):
    vacant = [i for i in range(9) if board[i] == -1]
    return random.choice(vacant)

def fatal(msg):
    print(msg)
    exit()

while True:
    game = GameServerAPI()
    
    err = True
    while err:
        my_id, err = game.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame') # TODO token ändern

    state, err = game.state()
    if err: fatal(err)

    while not state['gameover']:
        time.sleep(2)
        print_board(state['board'])

        if state['current'] == my_id: # my turn
            while True:
                pos = random_move(state['board'])
                err = game.move(position=pos)
                if err: print(err)
                else: break
        else:
            print("Opponent's turn ...")

        state, err = game.state()
        if err: fatal(err)
