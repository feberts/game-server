#!/usr/bin/env python3

# client for game server prototype

import api
import time

my_id, msg = api.join_game()
time.sleep(3) # TODO

if my_id == None:
    print('failed joining game:', msg)
    exit()

players = ('x', 'o')

def print_board(board):
    board = [i if board[i] == -1 else players[board[i]] for i in range(9)]
    print(f' {board[0]} | {board[1]} | {board[2]}', f'---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', f'---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def user_input(current):
    while True:
        try:
            return int(input(f'Your turn {players[current]}: '))
        except KeyboardInterrupt:
            exit()
        except:
            print('Integers only!')

state = api.state()

while not state.gameover:
    print_board(state.board)

    if state.current == my_id: # my turn
        while True:
            pos = user_input(state.current)
            ok = api.move(pos)
            if ok:
                break
            else:
                print('Illegal move!')
    else:
        print(f'Opponents turn {players[state.current]} ...')
        time.sleep(1)

    state = api.state()

print_board(state.board)

if state.winner == None:
    print('No winner!')
else:
    print(f'Player {players[state.winner]} wins!')
