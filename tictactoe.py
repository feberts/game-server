#!/usr/bin/env python3

board = list(range(9))
players = ('x', 'o')
current = 0

def print_board():
    print(f' {board[0]} | {board[1]} | {board[2]}', f'---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', f'---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def read_position():
    while True:
        try:
            pos = int(input(f'Player {players[current]}: '))
            if move_valid(pos):
                return pos
            else:
                print('Move illegal!')
        except KeyboardInterrupt:
            exit()
        except:
            print('Integers only!')

def move_valid(pos):
    return pos in board

def update_board(pos):
    board[pos] = players[current]

def check_win():
    for x, y, z in ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)):
        if board[x] == board[y] == board[z] == players[current]:
            print_board()
            print(f'Player {players[current]} wins!')
            exit()

while True:
    print_board()
    update_board(read_position())
    check_win()
    current ^= 1
