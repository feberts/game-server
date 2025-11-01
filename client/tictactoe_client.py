#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another
client. If you want to test it on a single machine, just run this program twice
in separate shells.
"""

from game_server_api import GameServerAPI

symbols = ('x', 'o')

def print_board(board):
    print('\n' * 100)
    board = [i if board[i] == -1 else symbols[board[i]] for i in range(9)]
    print(f' {board[0]} | {board[1]} | {board[2]}', '---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', '---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def user_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except KeyboardInterrupt:
            print('')
            exit()
        except ValueError:
            print('Integers only!')

def fatal(msg):
    print(msg)
    exit()

game = GameServerAPI(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame')

my_id, err = game.join_game()

if err: # no game started yet
    my_id, err = game.start_game(players=2)
    if err: fatal(err)

state, err = game.state(blocking=False)
if err: fatal(err)

while not state['gameover']:
    print_board(state['board'])

    if my_id in state['current']: # my turn
        while True:
            pos = user_input(f'\nYour ({symbols[my_id]}) turn: ')
            err = game.move(position=pos)
            if err: print(err)
            else: break
        blocking = False
    else:
        print("Opponent's turn ...")
        blocking = True

    state, err = game.state(blocking)
    if err: fatal(err)

print_board(state['board'])
winner = state['winner']

if winner is None:
    print('No winner...')
elif winner == my_id:
    print(f'You ({symbols[my_id]}) win!')
else:
    print(f'You ({symbols[my_id]}) lose...')
