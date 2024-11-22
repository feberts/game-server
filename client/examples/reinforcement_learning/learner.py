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

class MENACE:
    """
    Implementation of Donald Michie's Matchbox Educable Noughts and Crosses Engine (MENACE).
    """

    def __init__(self):
        self._boxes = {} # board layout -> list of empty positions
        self._current_game = {} # board layout -> chosen position
        self._stage = 0 # stage in the current game
        self._number_of_beads = [4, 3, 2, 1, 1] # initial beads of each colour per stage

    def move(self, board):
        layout = tuple(board)

        if layout not in self._boxes:
            # initialize box with coloured beads (in the US, use colored beads):
            coloured_beads = [i for i in range(9) if layout[i] == -1] # vacant positions
            self._boxes[layout] = coloured_beads * self._number_of_beads[self._stage]

        pos = random.choice(self._boxes[layout])
        self._current_game[layout] = pos # used for backpropagation
        self._stage += 1

        return pos

    def win(self):
        # backpropagation:
        for layout, pos in self._current_game.items():
            self._boxes[layout].append(pos) # old TODO
            #self._boxes[layout].extend([pos] * 3) # new TODO

        self._new_game()

    def loss(self):
        # backpropagation:
        for layout, pos in self._current_game.items():
            if len(self._boxes[layout]) > 1: # keep last remaining bead
                self._boxes[layout].remove(pos)
            #else:
                #del self._boxes[layout] # TODO works better?

        self._new_game()

    def draw(self):
        # backpropagation:
        #for layout, pos in self._current_game.items(): # new TODO
            #self._boxes[layout].extend([pos] * 1) # new TODO

        self._new_game()

    def _new_game(self):
        self._current_game = {}
        self._stage = 0

def fatal(msg):
    print(msg)
    exit()

class Statistic:
    def __init__(self):
        self.games = 0
        self.won = 0
        self.draw = 0
    def show(self):
        print(f'win: {self.won / self.games:.3f}',
              f'draw: {self.draw / self.games:.3f}')

game = GameServerAPI()

my_id, err = game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2)
if err: fatal(err)

menace = MENACE()
statistic = Statistic()
sample_size = 1000
samples_max = 10
samples = 0

start = time.time()

while samples < 1000:
    samples += 1
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
        statistic.won += 1
    elif winner == None:
        menace.draw()
        statistic.draw += 1
    else:
        menace.loss()

    game.reset_game()

    statistic.games += 1

    if statistic.games == sample_size:
        statistic.show()
        statistic = Statistic()

print(time.time() - start)
