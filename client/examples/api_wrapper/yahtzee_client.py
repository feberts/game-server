#!/usr/bin/env python3
"""
Yahtzee client.

This program connects to the game server to play Yahtzee, alone, or against
other clients.
"""

from yahtzee_api import YahtzeeAPI

def print_scorecard(scorecard):
    print('\n' * 100)
    print('Yahtzee\n')
    for category, points in scorecard.items():
        points = str(points) if points is not None else ''
        print(f'{category:16s}{points:_>3s}')

def print_dice(dice):
    print('')
    for d in dice:
        print(f'[{d}] ', end='')
    print('\n a   b   c   d   e')

def menu(options):
    print('\nOptions:')
    for i, opt in enumerate(options):
        print(f'{i:3} - {opt}')
    while True:
        try:
            option = int(input('\nYour option: '))
            if option < 0 or option >= len(options): raise ValueError
            return option
        except KeyboardInterrupt:
            print('')
            exit()
        except ValueError:
            print('Invalid option!')

def select_dice():
    selection = input('\nSelect one or more dice (e.g.: cde): ')
    indices = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4}
    dice = []
    for s in selection:
        dice.append(indices.get(s))
    return dice

def print_ranking(ranking):
    print('\nRanking:\n')
    ranking = list(ranking.items())
    ranking = sorted(ranking, key=lambda t: t[1], reverse=True)
    for name, points in ranking:
        print(f'{name:10s}{points:5}')

def fatal(msg):
    print(msg)
    exit()

game = YahtzeeAPI()

# join game:
my_id, err = game.join_game(token='mygame')

if err: # no game started yet
    # start new game:
    my_id, err = game.start_game(token='mygame', players=1)
    if err: fatal(err)

# submit name:
while True:
    err = game.submit_name(input('Enter name: '))
    if err: print(err)
    else: break

categories = ['Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes', 'Chance', 'Three of a Kind', 'Four of a Kind', 'Full House', 'Small Straight', 'Large Straight', 'Yahtzee']

state, err = game.state(blocking=False)
if err: fatal(err)

while not state.gameover:
    print_scorecard(state.scorecard)

    if state.my_turn:
        print_dice(state.dice)

        option = menu(['roll all dice again', 'roll some dice again', 'add points to scorecard', 'cross out a category'])

        if option == 0:
            err = game.roll_all_dice()
        elif option == 1:
            err = game.roll_some_dice(select_dice())
        elif option == 2:
            option = menu(categories)
            err = game.add_points(categories[option])
        elif option == 3:
            option = menu(categories)
            err = game.cross_out_category(categories[option])

        if err:
            print(err)
            input('\n<press enter>')

        blocking = False
    else:
        if state.current_name:
            print(f"\n{state.current_name}'s turn ...")
        else:
            print('\nOpponents are choosing their names...')
        blocking = True

    state, err = game.state(blocking=blocking)
    if err: fatal(err)

print_scorecard(state.scorecard)
print_ranking(state.ranking)
