#!/usr/bin/env python3

# The goal is to reduce the amount of code required for the client API. Instead of providing a separate move-function for each game, a generic function could be used, that accepts the arguments as named args. The move could then be sent to the server as a dictionary/json.

import json

data = None

##### CLIENT #####

class Api:
    def move(self, **kwargs): # generic api function
        print('Api.move()')
        for key, val in kwargs.items():
            print(key, '=', val)
        self._send_move(kwargs)

    def _send_move(self, move): # send move to server
        print('Api._send_move()')
        j = json.dumps(move)
        global data
        data = j
        print('json:', j)

api = Api()

api.move(piece='pawn', x='d', y=7) # pawn to D7


##### SERVER #####

class Game:
    def move(self, piece, x, y):
        print('Game.move()')
        print(f'piece = {piece}, x = {x}, y = {y}')

def receive_move():
    print('receive_move()')
    d = json.loads(data)
    print('dict: ', d)
    game.move(d['piece'], d['x'], d['y'])

game = Game()
receive_move()
