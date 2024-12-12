#!/usr/bin/env python3
"""
TODO Kommentar

Michael Maranan
https://thepythoncode.com/article/make-a-tic-tac-toe-game-pygame-in-python

Rockikz (GitHub user)
https://github.com/x4nth055/pythoncode-tutorials/tree/master/gui-programming/tictactoe-game
"""
import pygame
from pygame.locals import *
from game_server_api import GameServerAPI # feb

pygame.init()
pygame.font.init()

window_size = (450, 500)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tic Tac Toe")

def fatal(msg): # feb
    print(msg) # feb
    exit() # feb

class TicTacToe():

    def __init__(self, table_size):
        self.game = GameServerAPI() # feb
        self.my_id = None # feb
        # join game:
        self.my_id, err = self.game.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame') # feb

        if err: # no game started yet
            # start new game:
            self.my_id, err = self.game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2) # feb
            if err: fatal(err) # feb

        self.state, err = self.game.state(blocking=False) # feb
        if err: fatal(err) # feb

        self.table_size = table_size
        self.cell_size = table_size // 3
        self.table_space = 20

        self.marks = ('X', 'O') # feb
        self.player = None # feb
        self._change_player()
        self.winner = None
        self.taking_move = True
        self.running = True
        self.table = []
        for col in range(3):
            self.table.append([])
            for row in range(3):
                self.table[col].append("-")

        self.background_color = (255, 174, 66)
        self.table_color = (50, 50, 50)
        self.line_color = (190, 0, 10)
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

    def _change_player(self):
        self.state, err = self.game.state(blocking=False) # feb
        if err: fatal(err) # feb

        if 0 in self.state['current']: # feb
            self.player = "X" # feb
        else: # feb
            self.player = "O" # feb

    # processing clicks to move
    def _move(self, pos):
        try:
            x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
            if self.table[x][y] == "-":
                self.game.move(position=y * 3 + x) # feb
                self.table[x][y] = self.player
                self._change_player()
        except:
            print("Click inside the table only")
            raise

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
            self.strike() # feb
        else:
            screen.fill(self.background_color, (135, 445, 188, 35))

            if self.my_id in self.state['current']: # feb
                instr = f'Your ({self.marks[self.my_id]}) turn' # feb
            else: # feb
                instr = 'Opponent ... ' # feb
            instructions = self.font.render(instr, True, self.instructions_color,self.background_color)
            #instructions = self.font.render(f'{self.player} to move', True, self.instructions_color)
            screen.blit(instructions,(75,445))

    def strike(self):
        if self.state['gameover'] and self.state['winner'] is not None: # feb
            b = self.state['board']
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
        line_strike = pygame.draw.line(screen, self.line_color, [start_x, start_y], [end_x, end_y], 8)

    def draw_marks(self): # feb
        self.state, err = self.game.state(blocking=False) # feb
        if err: fatal(err) # feb
        for y in range(3): # feb
            for x in range(3): # feb
                player = self.state['board'][y * 3 + x] # feb
                if player in (0, 1): # feb
                    self._draw_char(x,y,player)

    def main(self):
        screen.fill(self.background_color)
        self._draw_table()

        while self.running:
            self.draw_marks() # feb
            self._message()

            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.running = False

                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    if self.taking_move:
                        self._move(self.event.pos)

            pygame.display.flip()
            self.FPS.tick(60)

            self.state, err = self.game.state(blocking=False) # feb
            if err: fatal(err) # feb
            self._change_player()

if __name__ == "__main__":
    g = TicTacToe(window_size[0])
    g.main()
