"""
TODO Kurzbeschreibung des Moduls.

TODO Ausfuehrliche Beschreibung des Moduls, ggf. ueber mehrere Zeilen.
"""

# api for game server used by the client

import socket
import json

IP = '127.0.0.1'
PORT = 4711
BUFFER_SIZE = 1024

class State:
    board = []
    current = 0
    gameover = False
    winner = None
    def __init__(self):
        self.board = [-1] * 9

player_id = None

def join_game():
    #print(f"Connecting to {IP}:{PORT} ...")
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sd.connect((IP, PORT))

    #print(f"Sending join request")
    write = bytes('join', 'utf-8')
    sd.sendall(write)

    read = sd.recv(BUFFER_SIZE)
    read = str(read, 'utf-8').strip()

    try:
        global player_id
        player_id = int(read)
        #print(f"Received player id: {str(player_id)}")
        return player_id, None
    except:
        #print(f"Received message: {read}")
        return None, read

def move(pos):
    #print(f"Connecting to {IP}:{PORT} ...")
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sd.connect((IP, PORT))

    #print(f"Sending move")
    write = bytes(f'move,{player_id},{pos}', 'utf-8')
    sd.sendall(write)

    read = sd.recv(BUFFER_SIZE)
    read = str(read, 'utf-8').strip()
    return read == 'ok'

def state():
    #print(f"Connecting to {IP}:{PORT} ...")
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sd.connect((IP, PORT))

    #print(f"Requesting state")
    write = bytes(f'state', 'utf-8')
    sd.sendall(write)

    read = sd.recv(BUFFER_SIZE)
    read = str(read, 'utf-8')
    read = json.loads(read)
    state = State()
    state.board = read['board']
    state.current = read['current']
    state.gameover = read['gameover']
    state.winner = read['winner']
    #print(f'Board: {state.board}, Type = {type(state.board)}')
    return state
