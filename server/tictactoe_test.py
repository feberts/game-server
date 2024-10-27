#!/usr/bin/env python3
"""
Interactive test of class TicTacToe.
"""

from tictactoe import TicTacToe

def print_board(board):
    board = [i if board[i] == -1 else players[board[i]] for i in range(9)]
    print(f' {board[0]} | {board[1]} | {board[2]}', '---+---+---',
          f' {board[3]} | {board[4]} | {board[5]}', '---+---+---',
          f' {board[6]} | {board[7]} | {board[8]}', sep='\n')

def user_input(current):
    while True:
        try:
            return int(input(f'Your turn {players[current]}: '))
        except KeyboardInterrupt:
            exit()
        except:
            print('Integers only!')

print('Min. players:', TicTacToe.min_players())
print('Max. players:', TicTacToe.max_players())

game = TicTacToe(2)
players = ('x', 'o')
current = game.current_player()
state = game.state(current)

while not state['gameover']:
    print_board(state['board'])

    while True:
        pos = user_input(current)
        err = game.move({'position':pos})
        if err:
            print(err)
        else:
            break

    state = game.state(current)
    current = game.current_player()

print_board(state['board'])
winner = state['winner']

if winner == None:
    print('No winner!')
else:
    print(f'Player {players[int(winner)]} wins!')
