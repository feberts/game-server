#!/usr/bin/env python3
"""
TODO Kurzbeschreibung des Moduls.

TODO Ausfuehrliche Beschreibung des Moduls, ggf. ueber mehrere Zeilen.
"""

# client for connecting to the game server

import api
import time

players = ('x', 'o')

def print_board(board):
    print('\n' * 100)
    print(f'Player {players[my_id]}')
    board = [i if board[i] == -1 else players[board[i]] for i in range(9)]
    print(f' {board[0]} | {board[1]} | {board[2]}', f'---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', f'---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def user_input(current):
    while True:
        try:
            return int(input(f'Your turn: '))
        except KeyboardInterrupt:
            exit()
        except:
            print('Integers only!')

my_id, msg = api.join_game()

if my_id == None:
    print('failed joining game:', msg)
    exit()

state = None

while True:
    try:
        state = api.state()
        break
    except:
        print('Waiting for game to start ...')
        time.sleep(1)

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
        print('Opponents turn ...')
        time.sleep(1)

    state = api.state()

print_board(state.board)

if state.winner == None:
    print('No winner!')
else:
    print(f'Player {players[state.winner]} wins!')
