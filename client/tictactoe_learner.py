#!/usr/bin/env python3
"""
TODO
"""

from game_server_api import GameServerAPI
import threading
import time

import threading
import time

from game_server_api import GameServerAPI

server = '127.0.0.1'
port = 4711
game = 'TicTacToe'
token = 'mygame2'
players = 2

def fatal(msg):
    print(msg)
    exit()
    
class Player:
    def __init__(self):
        self._api = GameServerAPI()

    def join(self):
        # join game:
        my_id, err = self._api.join_game(server, port, game, token)

        if err: # no game started yet
            # start new game:
            my_id, err = self._api.start_game(server, port, game, token, players)
            if err: fatal(err)

class RandomPlayer(Player):
    def __init__(self):
        super().__init__()
        pass

class LearningPlayer(Player):
    def __init__(self):
        super().__init__()
        pass

random_player = RandomPlayer()
learning_player = LearningPlayer()


def join(player):
    player.join()

threading.Thread(target=join, args=(random_player,), daemon=True).start()
time.sleep(1)
threading.Thread(target=join, args=(learning_player,), daemon=True).start()
time.sleep(1)

"""
def client_start():
    api = GameServerAPI()
    my_id, err = api.start_game(server=server, port=port, game=game, token=token, players=players, name='Bob')

    if err:
        print(err)
        exit()

    print('Player ID Bob:', my_id)

def client_join():
    api = GameServerAPI()
    my_id, err = api.join_game(server=server, port=port, game=game, token=token, name='Alice')

    if err:
        print(err)
        exit()

    print('Player ID Alice:', my_id)

def client_watch():
    api = GameServerAPI()
    my_id, err = api.watch(server=server, port=port, game=game, token=token, name='Alice')

    if err:
        print(err)
        exit()

    print('Observed ID:', my_id)

#threading.Thread(target=client_start, args=(), daemon=True).start()
time.sleep(0.1)
#threading.Thread(target=client_join, args=(), daemon=True).start()
time.sleep(0.1)
#threading.Thread(target=client_watch, args=(), daemon=True).start()

#for _ in range(players):
    #threading.Thread(target=client_join, args=(), daemon=True).start()

time.sleep(1)
"""




"""
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



supervisor = GameServerAPI()

# join game:
my_id, err = supervisor.join_game(server, port, game, token)

if err: # no game started yet
    # start new game:
    my_id, err = supervisor.start_game(server, port, game, token, players=2)
    if err: fatal(err)

state, err = supervisor.state()
if err: fatal(err)

while not state['gameover']:
    print_board(state['board'])

    if state['current'] == my_id: # my turn
        while True:
            pos = user_input(f'\nYour ({symbols[my_id]}) turn: ')
            err = supervisor.move(position=pos)
            if err: print(err)
            else: break
    else:
        print("Opponent's turn ...")
        time.sleep(0.5)

    state, err = supervisor.state()
    if err: fatal(err)

print_board(state['board'])
winner = state['winner']

if winner == None:
    print('No winner...')
elif winner == my_id:
    print(f'You ({symbols[my_id]}) win!')
else:
    print(f'You ({symbols[my_id]}) lose...')
"""
