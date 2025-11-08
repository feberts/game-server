#!/usr/bin/env python3
"""
Echo!

Not really a game, but occasionally useful for debugging and testing.

An unmodified copy of the data sent to the server is sent back to the client.
The game is over as soon as the message 'quit' is sent.
"""

from game_server_api import GameServerAPI

def fatal(msg):
    print(msg)
    exit()

game = GameServerAPI(server='127.0.0.1', port=4711, game='Echo', token='mygame')

my_id, err = game.start_game(players=1)
if err: fatal(err)

state, err = game.state()
if err: fatal(err)

while not state['gameover']:
    err = game.move(msg=input('Message: '))
    if err: fatal(err)

    state, err = game.state()
    if err: fatal(err)

    print('Echo:   ', state['echo'])
