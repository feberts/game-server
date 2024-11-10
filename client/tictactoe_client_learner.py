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

class MENACE:
    """
    Implementation of Donald Michie's device.
    """
    def __init__(self):
        self.boxes = {} # board layout -> list of possible positions
        self.current_game = {} # board layout -> chosen position
        self.stage = 0 # stage in the current game
        self.n_beads = [4, 3, 2, 1, 1] # initial number of beads per game stage and colour

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
        for layout, pos in self.current_game.items():
            self.boxes[layout].append(pos) # old
            #self.boxes[layout].extend([pos] * 3) # new
        self.new_game()

    def loose(self):
        for layout, pos in self.current_game.items():
            if len(self.boxes[layout]) > 1: # keep last bead 
                self.boxes[layout].remove(pos)
            #else:
                #del self.boxes[layout] # TODO makes sense?
        self.new_game()

    def draw(self):
        #for layout, pos in self.current_game.items(): # new
            #self.boxes[layout].extend([pos] * 1) # new
        self.new_game()
        
    def new_game(self):
        self.current_game = {}
        self.stage = 0

game = GameServerAPI()
my_id, err = game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='learn', players=2)
if err: fatal(err)

stat = Statistic()
menace = MENACE()
reinforcements = 0

while stat.games < 10000:
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

    if winner == my_id:
        reinforcements += 1
        #stat.won += 1
        menace.win()
    elif winner == None:
        reinforcements += 0
        #stat.draw += 1
        menace.draw()
    else:
        reinforcements -= 1
        #stat.lost += 1
        menace.loose()

    game.reset_game()
    print(stat.games, reinforcements, sep=',')
    
#stat.show()
#print(''.join(outcome))
#print(menace.current_game)
