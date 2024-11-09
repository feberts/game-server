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

class Statistic:
    def __init__(self):
        self.games = 0
        self.won = 0
        self.lost = 0
        self.draw = 0
    def show(self):
        print(f'games: {self.games:3}, win rate: {self.won / self.games:.3f}, draw rate: {self.draw / self.games:.3f}, won: {self.won}, lost: {self.lost}, draw: {self.draw}')

class Menace:
    def __init__(self):
        self.matchboxes = {} # board configuration -> list of positions
        self.game = {} # board configuration -> position
        self.stage = 0 # stage in a game

    def move(self, board):
        board = tuple(board)
        if board not in self.matchboxes:
            vacant = [i for i in range(9) if board[i] == -1] * (5 - self.stage)
            self.matchboxes[board] = vacant
        pos = random.choice(self.matchboxes[board])
        self.game[board] = pos
        self.stage += 1
        return pos
    
    def reset(self):
        self.game = {}
        self.stage = 0
    
    def win(self):
        for configuration, move in self.game.items():
            #print(configuration, '->', move)
            self.matchboxes[configuration].append(move)
        self.reset()

    def loose(self):
        for configuration, move in self.game.items():
            #print(configuration, '->', move)
            if len(self.matchboxes[configuration]) > 1: # keep last bead # TODO makes sense?
                self.matchboxes[configuration].remove(move)
        self.reset()

    def draw(self):
        self.reset()
        

game = GameServerAPI()
my_id, err = game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='learn', players=2)
if err: fatal(err)

stat = Statistic()
menace = Menace()

while stat.games < 1000:
    state, err = game.state()
    if err: fatal(err)

    while not state['gameover']:
        if state['current'] == my_id:
            pos = menace.move(state['board'])
            err = game.move(position=pos)
            if err: fatal(err)

        state, err = game.state()
        if err: fatal(err)

    winner = state['winner']
    stat.games += 1

    if winner == None:
        #print('draw')
        stat.draw += 1
        menace.draw()
    elif winner == my_id:
        #print('won ')
        stat.won += 1
        menace.win()
    else:
        #print('lost')
        stat.lost += 1
        menace.loose()
        
    game.reset_game()
    
stat.show()
#print(menace.game)
