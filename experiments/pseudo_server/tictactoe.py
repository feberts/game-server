#!/usr/bin/env python3

# a straightforward tic-tac-toe implementation

board = list(range(9))
players = ('x', 'o')
current = 0

def print_board():
    print(f' {board[0]} | {board[1]} | {board[2]}', f'---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', f'---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def user_input():
    while True:
        try:
            pos = int(input(f'Player {players[current]}: '))
            if move_valid(pos):
                return pos
            else:
                print('Illegal move!')
        except KeyboardInterrupt:
            exit()
        except:
            print('Integers only!')

def move_valid(pos):
    return pos in board

def update_board(pos):
    board[pos] = players[current]

def check_win():
    for i, j, k in ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)):
        if board[i] == board[j] == board[k] == players[current]:
            print_board()
            print(f'Player {players[current]} wins!')
            exit()

for _ in range(9):
    print_board()
    update_board(user_input())
    check_win()
    current ^= 1 # rotate players

print_board()
print('No winner!')
