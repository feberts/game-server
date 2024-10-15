#!/usr/bin/env python3

# The goal is to reduce the amount of code required for the client API. Instead of providing a separate move-function for each game (or even multiple functions for a single game), a generic function could be used, that accepts the arguments as keyword args. The move could then be sent to the server as a JSON-object/dictionary.

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

class Server:
    class Game:
        def move(self, args):
            piece, x, y, = args['piece'], args['x'], args['y']
            print('Game.move()')
            print(f'piece = {piece}, x = {x}, y = {y}')

    game = Game()
    
    def receive_move(self):
        print('receive_move()')
        d = json.loads(data)
        print('dict: ', d)
        self.game.move(d)

server = Server()
server.receive_move()
