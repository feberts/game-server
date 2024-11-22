#!/usr/bin/env python3
"""
Tic-tac-toe learner.

This client learns how to play tic-tac-toe. It uses a method designed by Donald Michie in 1961 to develop a strategy. During training, a statistic is printed showing how the performance improves over time.

Article by Donald Michie describing his method: https://academic.oup.com/comjnl/article/6/3/232/360077

Wikipedia article on his method: https://en.wikipedia.org/w/index.php?title=Matchbox_Educable_Noughts_and_Crosses_Engine&oldid=1242708397
"""

import random
import time

from game_server_api import GameServerAPI

# TODO aufräumen

class MENACE:
    """
    Implementation of Donald Michie's Matchbox Educable Noughts and Crosses Engine (MENACE).
    """

    def __init__(self):
        self.boxes = {} # board layout -> list of possible positions
        self.current_game = {} # board layout -> chosen position
        self.stage = 0 # stage in the current game
        self.n_beads = [4, 3, 2, 1, 1] # initial number of beads of the same colour per game stage

    def move(self, board):
        layout = tuple(board)
        if layout not in self.boxes:
            vacant = [i for i in range(9) if layout[i] == -1]
            self.boxes[layout] = vacant * self.n_beads[self.stage]
        pos = random.choice(self.boxes[layout])
        self.current_game[layout] = pos
        self.stage += 1
        return pos

    def win(self):
        # backpropagation:
        for layout, pos in self.current_game.items():
            self.boxes[layout].append(pos) # old TODO
            #self.boxes[layout].extend([pos] * 3) # new TODO
        self.new_game()

    def loose(self):
        # backpropagation:
        for layout, pos in self.current_game.items():
            if len(self.boxes[layout]) > 1: # keep last remaining bead
                self.boxes[layout].remove(pos)
            #else:
                #del self.boxes[layout] # TODO works better?
        self.new_game()

    def draw(self):
        # backpropagation:
        #for layout, pos in self.current_game.items(): # new TODO
            #self.boxes[layout].extend([pos] * 1) # new TODO
        self.new_game()

    def new_game(self):
        self.current_game = {}
        self.stage = 0

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
        print(f'win: {self.won / self.games:.3f}',
              f'draw: {self.draw / self.games:.3f}')

game = GameServerAPI()
my_id, err = game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2)
if err: fatal(err)

menace = MENACE()
stat = Statistic()
reinforcements = 0
start = time.time()
n = 0
while n < 1000:
    n += 1
    state, err = game.state()
    if err: fatal(err)

    while not state['gameover']:
        if my_id in state['current']:
            pos = menace.move(state['board'])
            err = game.move(position=pos)
            if err: fatal(err)

        state, err = game.state()
        if err: fatal(err)

    winner = state['winner']

    if winner == my_id:
        menace.win()
        stat.won += 1
        reinforcements += 1
    elif winner == None:
        menace.draw()
        stat.draw += 1
        reinforcements += 0
    else:
        menace.loose()
        stat.lost += 1
        reinforcements -= 1

    game.reset_game()

    stat.games += 1
    if stat.games == 1000:
        stat.show()
        stat = Statistic()
    #print(stat.games, reinforcements, sep=',')

#print(''.join(outcome))
#print(menace.current_game)
print(time.time() - start)
