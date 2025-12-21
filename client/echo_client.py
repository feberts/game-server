#!/usr/bin/env python3
"""
Echo!

Not really a game, but occasionally useful for debugging and testing.

An unmodified copy of the data sent to the server is sent back to the client.
The game is over as soon as the message 'quit' is sent.
"""

from game_server_api import GameServerAPI, GameError

game = GameServerAPI(server='127.0.0.1', port=4711, game='Echo', token='mygame', players=1)

my_id = game.join()

state = game.state()

while not state['gameover']:
    try:
        game.move(msg=input('Message: '))
    except GameError as e:
        print(e)

    state = game.state()

    print('Echo:   ', state['echo'])
