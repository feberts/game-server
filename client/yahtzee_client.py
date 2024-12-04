#!/usr/bin/env python3
"""
Yahtzee client.

This program connects to the game server to play Yahtzee, alone, or against other clients.
"""

from game_server_api import GameServerAPI

def print_scorecard(scorecard):
    print('\n' * 100)
    print('Your score:\n')
    for combination, score in scorecard.items():
        score = str(score) if score != None else ''
        print(f"{combination:10s}{score:_>3s}")

def print_dice(dice):
    print('')
    for d in dice:
        print(f'[{d}] ', end='')
    print('\n a   b   c   d   e')

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

combinations = ['Ones', 'Twos', 'Threes']

def select_dice():
    selection = input('Select one or more dice (e.g.: cde): ')
    indices = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4}
    dice = []
    for s in selection:
        dice.append(indices.get(s))
    return dice
    

while not state['gameover']:
    print_scorecard(state['scorecard'])

    if my_id in state['current']: # my turn
        print_dice(state['dice'])
        
        while True:
            option = menu(['roll all dice again', 'roll some dice again', 'add points to score', 'cross out a combination'])

            if option == 0:
                err = game.move(roll_dice='all')
            elif option == 1:
                err = game.move(roll_dice=select_dice())
            elif option == 2:
                option = menu(combinations)
                err = game.move(score='add points', combination=combinations[option])
            elif option == 3:
                option = menu(combinations)
                err = game.move(score='cross out', combination=combinations[option])

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
