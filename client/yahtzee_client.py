#!/usr/bin/env python3
"""
Yahtzee client.

This program connects to the game server to play Yahtzee, alone, or against other clients.
"""

from game_server_api import GameServerAPI

def print_scorecard(scorecard):
    print('\n' * 100)
    print('Your score:')
    for combination, score in scorecard.items():
        score = str(score) if score else '___'
        print(f"{combination:10s}{score:>4s}")

def print_dice(dice):
    print('')
    for d in dice:
        print(f'[{d}] ', end='')
    print('\n a   b   c   d   e')
"""
def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except KeyboardInterrupt:
            exit()
        except:
            print('Invalid option!')
"""

def menu(options):
    print('\nOptions:')
    for i in range(len(options)):
        print(f'{i:3} - {options[i]}')
    while True:
        try:
            option = int(input('\nYour option: '))
            if option < 0 or option >= len(options): raise Exception
            return option
        except KeyboardInterrupt:
            exit()
        except:
            print('Invalid option!')
        
def fatal(msg):
    print(msg)
    exit()

game = GameServerAPI()

# join game:
my_id, err = game.join_game(server='127.0.0.1', port=4711, game='Yahtzee', token='mygame')

if err: # no game started yet
    # start new game:
    my_id, err = game.start_game(server='127.0.0.1', port=4711, game='Yahtzee', token='mygame', players=1)
    if err: fatal(err)

state, err = game.state(blocking=False)
if err: fatal(err)

while not state['gameover']:
    print_scorecard(state['scorecard'])

    if my_id in state['current']: # my turn
        print_dice(state['dice'])
        
        while True:
            option = menu(['roll all dice again', 'roll some dice', 'add to Ones', 'add to Twos', 'add to Threes'])
            if option == 0: err = game.move(roll='all')
            if err: print(err)
            else: break
        blocking = False
    else:
        print("Opponent's turn ...")
        blocking = True

    state, err = game.state(blocking)
    if err: fatal(err)

print_scorecard(state['scorecard'])

print('end')
