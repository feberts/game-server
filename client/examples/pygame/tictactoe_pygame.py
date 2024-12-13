#!/usr/bin/env python3
"""
This is a graphical tic-tac-toe client using Pygame (www.pygame.org). It is based on an implementation found on GitHub.

The original implementation is a stand-alone program to be used by two human players on the same machine. It was reworked by me (Fabian Eberts) to use my game server API and play against a remote client. Most of the game logic was removed and replaced by calls to API functions.

Code added by me is marked with a 'feb' comment.


Source of the original implementation:
GitHub user 'x4nth055' (Rockikz)
https://github.com/x4nth055/pythoncode-tutorials/tree/master/gui-programming/tictactoe-game
Accessed: 2024-12-12

The implementation is also presented on this website:
Author: Michael Maranan
https://thepythoncode.com/article/make-a-tic-tac-toe-game-pygame-in-python
Accessed: 2024-12-12

The two PNG files were downloaded from the same website.


MIT License

Copyright (c) 2019 Rockikz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
"""

import pygame
from pygame.locals import *
import threading # feb
from game_server_api import GameServerAPI # feb

pygame.init()
pygame.font.init()

window_size = (450, 500)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tic Tac Toe")

def fatal(msg): # feb (function)
    print(msg)
    exit()

class TicTacToe():

    def __init__(self, table_size):
        # feb start
        self.game = GameServerAPI()
        self.my_id = None

        # join game:
        self.my_id, err = self.game.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame')

        if err: # no game started yet
            # start new game:
            self.my_id, err = self.game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2)
            if err: fatal(err)

        self.state, err = self.game.state(blocking=False)
        if err: fatal(err)

        self.marks = ('X', 'O')
        self._sending_move = threading.Event()
        # feb end

        self.table_size = table_size
        self.cell_size = table_size // 3
        self.table_space = 20

        self.background_color = (255, 174, 66)
        self.table_color = (50, 50, 50)
        self.line_color = (0, 175, 0)
        self.instructions_color = (17, 53, 165)
        self.game_over_bg_color = (47, 98, 162)
        self.game_over_color = (255, 179, 1)
        self.font = pygame.font.SysFont("Courier New", 35)
        self.FPS = pygame.time.Clock()

    # draws table representation
    def _draw_table(self):
        tb_space_point = (self.table_space, self.table_size - self.table_space)
        cell_space_point = (self.cell_size, self.cell_size * 2)
        r1 = pygame.draw.line(screen, self.table_color, [tb_space_point[0], cell_space_point[0]], [tb_space_point[1], cell_space_point[0]], 8)
        c1 = pygame.draw.line(screen, self.table_color, [cell_space_point[0], tb_space_point[0]], [cell_space_point[0], tb_space_point[1]], 8)
        r2 = pygame.draw.line(screen, self.table_color, [tb_space_point[0], cell_space_point[1]], [tb_space_point[1], cell_space_point[1]], 8)
        c2 = pygame.draw.line(screen, self.table_color, [cell_space_point[1], tb_space_point[0]], [cell_space_point[1], tb_space_point[1]], 8)

    # processing clicks to move
    def _move(self, pos):
        try:
            x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
            self.game.move(position=y * 3 + x) # feb
        except:
            print("Click inside the table only")

    # draws character of the recent player to the selected table cell
    def _draw_char(self, x, y, player):
        if player == 0:
            img = pygame.image.load("mark_x.png")
        elif player == 1:
            img = pygame.image.load("mark_o.png")
        img = pygame.transform.scale(img, (self.cell_size, self.cell_size))
        screen.blit(img, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    # instructions and game-state messages
    def _message(self):
        if self.state['gameover']: # feb
            screen.fill(self.game_over_bg_color, (135, 445, 188, 35))
            if self.state['winner'] == self.my_id: # feb
                msg = f'You ({self.marks[self.my_id]}) win! ' # feb
            elif self.state['winner'] is None: # feb
                msg = 'No winner ...' # feb
            else: # feb
                msg = f'You ({self.marks[self.my_id]}) lose...' # feb
            msg = self.font.render(msg, True, self.instructions_color,self.background_color)
            screen.blit(msg,(75,445))
            self._strike()
        else:
            screen.fill(self.background_color, (135, 445, 188, 35))

            if self.my_id in self.state['current']: # feb
                instr = f'Your ({self.marks[self.my_id]}) turn' # feb
            else: # feb
                instr = 'Opponent ... ' # feb
            instructions = self.font.render(instr, True, self.instructions_color,self.background_color)
            screen.blit(instructions,(75,445))

    def _strike(self):
        if self.state['gameover'] and self.state['winner'] is not None: # feb
            b = self.state['board'] # feb
            if b[0] == b[1] == b[2] and b[2] != -1:
                self._pattern_strike((0,0),(2,0),"hor")
            elif b[3] == b[4] == b[5] and b[5] != -1:
                self._pattern_strike((0,1),(2,1),"hor")
            elif b[6] == b[7] == b[8] and b[8] != -1:
                self._pattern_strike((0,2),(2,2),"hor")
            elif b[0] == b[3] == b[6] and b[6] != -1:
                self._pattern_strike((0,0),(0,2),"ver")
            elif b[1] == b[4] == b[7] and b[7] != -1:
                self._pattern_strike((1,0),(1,2),"ver")
            elif b[2] == b[5] == b[8] and b[8] != -1:
                self._pattern_strike((2,0),(2,2),"ver")
            elif b[0] == b[4] == b[8] and b[8] != -1:
                self._pattern_strike((0,0),(2,2),"left-diag")
            elif b[2] == b[4] == b[6] and b[6] != -1:
                self._pattern_strike((2,0),(0,2),"right-diag")

    # strikes a line to winning patterns if already has
    def _pattern_strike(self, start_point, end_point, line_type):
        # gets the middle value of the cell
        mid_val = self.cell_size // 2

        # for the vertical winning pattern
        if line_type == "ver":
            start_x, start_y = start_point[0] * self.cell_size + mid_val, self.table_space
            end_x, end_y = end_point[0] * self.cell_size + mid_val, self.table_size - self.table_space

        # for the horizontal winning pattern
        elif line_type == "hor":
            start_x, start_y = self.table_space, start_point[-1] * self.cell_size + mid_val
            end_x, end_y = self.table_size - self.table_space, end_point[-1] * self.cell_size + mid_val

        # for the diagonal winning pattern from top-left to bottom right
        elif line_type == "left-diag":
            start_x, start_y = self.table_space, self.table_space
            end_x, end_y = self.table_size - self.table_space, self.table_size - self.table_space

        # for the diagonal winning pattern from top-right to bottom-left
        elif line_type == "right-diag":
            start_x, start_y = self.table_size - self.table_space, self.table_space
            end_x, end_y = self.table_space, self.table_size - self.table_space

        # draws the line strike
        line_strike = pygame.draw.line(screen, self.line_color, [start_x, start_y], [end_x, end_y], 16)

    def _draw_marks(self):
        for y in range(3):
            for x in range(3):
                player = self.state['board'][y * 3 + x] # feb
                if player in (0, 1): # feb
                    self._draw_char(x,y,player)

    def _request_state(self): # feb (function)
        blocking = True
        while True:
            self.state, err = self.game.state(blocking=blocking)
            blocking = True
            if err: fatal(err)
            if self.my_id in self.state['current']:
                self._sending_move.clear()
                self._sending_move.wait()
                blocking = False
            if self.state['gameover']:
                return

    def main(self):
        screen.fill(self.background_color)
        self._draw_table()
        running = True
        threading.Thread(target=self._request_state, args=(), daemon=True).start() # feb

        while running:
            self._draw_marks()
            self._message()

            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    running = False

                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    self._move(self.event.pos)
                    self._sending_move.set()

            pygame.display.flip()
            self.FPS.tick(60)

if __name__ == "__main__":
    g = TicTacToe(window_size[0])
    g.main()
