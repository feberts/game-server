#!/usr/bin/env python3

# game server

import game
import socket
#import pickle
import json

IP = '127.0.0.1'
PORT = 4711
BUFFER_SIZE = 1024

def wait_for_player(player_id):
    print('Waiting for join request ...')
    joined = False
    ip, port = None, None

    while not joined:
        conn, client = sd.accept()
        ip, port = client
        print(f'Accepted connection from {ip}:{port}')

        read = conn.recv(BUFFER_SIZE)
        request = str(read, 'utf-8')
        print(f"Received data from {ip}:{port}: {request}")

        if request == 'join':
            print(f'Received join request from {ip}:{port}')
            print(f"Sending player id to {ip}:{port}: {player_id}")
            conn.sendall(bytes(str(player_id), 'utf-8'))
            joined = True
        else:
            print(f'Received invalid request from {ip}:{port}')
            print(f"Sending error message to {ip}:{port}")
            conn.sendall(bytes('error: invalid request', 'utf-8'))

        conn.close()
        print(f"Closed connection to {ip}:{port}")

    return ip, port

try:
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sd.bind((IP, PORT))
    sd.listen()
    print(f'Listening on {IP}:{PORT}')

    wait_for_player(0)
    wait_for_player(1)

    game = game.Game()

    while True:
        conn, client = sd.accept()
        ip, port = client
        print(f'Accepted connection from {ip}:{port}')
        read = conn.recv(BUFFER_SIZE)
        print(f"Received data from {ip}:{port}: {read}")

        request = str(read, 'utf-8').split(',')

        if 'move' in request:
            _, player_id, pos = request
            player_id = int(player_id)
            pos = int(pos)
            print(f'Received move request (player id: {player_id}, position: {pos})')
            if game.state().current == player_id:
                ok = game.move(pos)
                if ok:
                    print('move valid')
                    conn.sendall(bytes('ok', 'utf-8'))
                else:
                    print('move not valid')
                    conn.sendall(bytes('err', 'utf-8'))
            else:
                print('wrong player')
                conn.sendall(bytes('err', 'utf-8'))
        elif 'state' in request:
            print('Player requesting state, sending state')
            #state = pickle.dumps(game.state())
            state = json.dumps(game.state_json())
            conn.sendall(bytes(state, 'utf-8'))
        else:
            print('Bad request')

        conn.close()
        print(f"Closed connection to {ip}:{port}")

        s = game.state()
        print(f'State: board: {s.board}, current: {s.current}, gameover: {s.gameover}, winner: {s.winner}')
except KeyboardInterrupt:
    try: conn.close()
    except: pass
finally:
    sd.close()
    print('\nServer shut down')
