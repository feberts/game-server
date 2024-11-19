#!/usr/bin/env python3
"""
Interactive local test of class TicTacToe.
"""

from tictactoe import TicTacToe

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
            exit()
        except:
            print('Integers only!')

print('Min. players:', TicTacToe.min_players())
print('Max. players:', TicTacToe.max_players())

game = TicTacToe(2)
current = game.current_player()[0]
state = game.state(current)

while not game.game_over():
    print_board(state['board'])

    while True:
        pos = user_input(f'Your turn {symbols[current]}: ')
        err = game.move({'position':pos}, current)
        if err:
            print(err)
        else:
            break

    state = game.state(current)
    current = game.current_player()[0]

print_board(state['board'])
winner = state['winner']

if winner == None:
    print('No winner!')
else:
    print(f'Player {symbols[winner]} wins!')
