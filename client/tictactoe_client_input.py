#!/usr/bin/env python3
"""
Tic-tac-toe input client.TODO

This program connects to the game server to play tic-tac-toe against another client. If you want to test it on a single machine, just run this program twice in separate shells.TODO
"""

from game_server_api import GameServerAPI
import time

def user_input(player_id):
    while True:
        try:
            return int(input(f'\nYour turn: '))
        except KeyboardInterrupt:
            exit()
        except:
            print('Integers only!')

def fatal(msg):
    print(msg)
    exit()

game = GameServerAPI()

# join game:
my_id, err = game.join_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', name='bob')

if err: # no game started yet
    # start new game:
    my_id, err = game.start_game(server='127.0.0.1', port=4711, game='TicTacToe', token='mygame', players=2, name='bob')
    if err: fatal(err)

state, err = game.state()
if err: fatal(err)

while not state['gameover']:
    if state['current'] == my_id: # my turn
        pos = user_input(my_id)
        err = game.move(position=pos)
        if err: print(err)

    time.sleep(0.5)
    state, err = game.state()
    if err: fatal(err)
