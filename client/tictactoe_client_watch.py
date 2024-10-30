#!/usr/bin/env python3
"""
Tic-tac-toe client.

This program connects to the game server to play tic-tac-toe against another client. If you want to test it on a single machine, just run this program twice in separate shells.
"""

from game_server_api import GameServerAPI
import time

def print_board(board):
    print('\n' * 100)
    board = [i if board[i] == -1 else players[board[i]] for i in range(9)]
    print(f' {board[0]} | {board[1]} | {board[2]}', '---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', '---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def fatal(msg):
    print(msg)
    exit()

players = ('x', 'o')
game = GameServerAPI()

# join a game as observer:
observed_id, err  = game.watch(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame')
if err: fatal(err)
print('ID:', observed_id)
exit() #TODO weg

state, err = game.state()
if err: fatal(err)
current_player = state['current']

while not state['gameover']:
    print_board(state['board'])

    if current_player == my_id: # my turn
        while True:
            pos = user_input(my_id)
            err = game.move(position=pos)
            if err: print(err)
            else: break
    else:
        print('Opponents turn ...')
        time.sleep(1)

    state, err = game.state()
    if err: fatal(err)
    current_player = state['current']

print_board(state['board'])
winner = state['winner']

if winner == None:
    print('No winner...')
elif winner == my_id:
    print(f'You ({players[my_id]}) won!')
else:
    print(f'You ({players[my_id]}) lost...')
