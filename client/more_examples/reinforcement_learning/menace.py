"""
MENACE implementation.

This module provides a reinforcement learning agent that learns how to play
tic-tac-toe. It uses a method designed by British researcher Donald Michie in
1961 to develop a strategy.

Article by Donald Michie describing his method:
https://academic.oup.com/comjnl/article/6/3/232/360077

Wikipedia article on his method: https://en.wikipedia.org/w/index.php?title=Matchbox_Educable_Noughts_and_Crosses_Engine&oldid=1242708397
"""

import random

class MENACE:
    """
    Implementation of Donald Michie's Matchbox Educable Noughts and Crosses
    Engine (MENACE).
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
            self._boxes[layout].append(pos) # add one bead to box
            # self._boxes[layout].extend([pos] * 3) # add three beads to box

        self._new_game()

    def loss(self):
        # backpropagation:
        for layout, pos in self._current_game.items():
            if len(self._boxes[layout]) > 1:
                self._boxes[layout].remove(pos) # remove one bead from box
            else:
                del self._boxes[layout] # reset box after last bead is removed

        self._new_game()

    def draw(self):
        # backpropagation:
        # for layout, pos in self._current_game.items():
            # self._boxes[layout].append(pos) # add one bead to box

        self._new_game()

    def _new_game(self):
        self._current_game = {}
        self._stage = 0
