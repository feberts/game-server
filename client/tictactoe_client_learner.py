#!/usr/bin/env python3
"""
Tic-tac-toe learner.

This client learns how to play tic-tac-toe. It collects data for reinforcement learning by performing random moves against another client and uses a method designed by Donald Michie in 1961 to develop a strategy. During training, a statistic is printed showing how the winning rate increases with more data.

Paper by Michie describing his method:
https://people.csail.mit.edu/brooks/idocs/matchbox.pdf
# TODO pdf in besserer qualität verfügbar?

Wikipedia article on his method:
https://en.wikipedia.org/w/index.php?title=Matchbox_Educable_Noughts_and_Crosses_Engine&oldid=1242708397
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
    global games, won, lost, draw
    print(f'games: {games}, won: {won}, lost: {lost}, draw: {draw}')

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

while games < 10000:
    state, err = game.state()
    if err: fatal(err)

    while not state['gameover']:
        #print_board(state['board'])

        if state['current'] == my_id:
            pos = random_move(state['board'])
            err = game.move(position=pos)
            if err: fatal(err)

        state, err = game.state()
        if err: fatal(err)

    #print_board(state['board'])
    winner = state['winner']
    
    games += 1

    if winner == None:
        draw += 1
        #print('No winner...')
    elif winner == my_id:
        won += 1
        #print(f'You ({symbols[my_id]}) win!')
    else:
        lost += 1
        #print(f'You ({symbols[my_id]}) lose...')
        
    #time.sleep(1)
    game.reset_game()

print(f'games: {games}, won: {won}, lost: {lost}, draw: {draw}, win rate: {won / games}, win rate opponent: {lost / games}')
