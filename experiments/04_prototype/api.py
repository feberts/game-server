#!/usr/bin/env python3

# api for game server prototype

import socket
import pickle

IP = '127.0.0.1'
PORT = 4711
BUFFER_SIZE = 1000000

player_id = None

def join_game():
    print(f"Connecting to {IP}:{PORT} ...")
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sd.connect((IP, PORT))
    
    print(f"Sending join request")
    write = bytes('join', 'utf-8')
    sd.sendall(write)
    
    read = sd.recv(BUFFER_SIZE)
    read = str(read, 'utf-8').strip()
    try:
        global player_id
        player_id = int(read)
        print(f"Received player id: {str(player_id)}")
        return player_id, None
    except:
        print(f"Received message: {read}")
        return None, read

def move(pos):
    print(f"Connecting to {IP}:{PORT} ...")
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sd.connect((IP, PORT))
    
    print(f"Sending move")
    write = bytes(f'move,{player_id},{pos}', 'utf-8')
    sd.sendall(write)
    
    read = sd.recv(BUFFER_SIZE)
    read = str(read, 'utf-8').strip()
    return read == 'ok'
    
# TODO nicht nötig?
#class State:
    #board = [-1] * 9
    #current = 0
    #gameover = False
    #winner = None
    
def state():
    print(f"Connecting to {IP}:{PORT} ...")
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sd.connect((IP, PORT))
    
    print(f"Requesting state")
    write = bytes(f'state', 'utf-8')
    sd.sendall(write)
    
    read = sd.recv(BUFFER_SIZE)
    state = pickle.loads(read)
    print(f'Board: {state.board}, Type = {type(state.board)}')
    return state
    

'''


print(f"Connecting to {IP}:{PORT} ...")
sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sd.connect((IP, PORT))
print('connected')

while True:
    write = input('Enter a word: ')
    print(f"Sending data: {write}")
    write = bytes(write, 'utf-8')
    sd.sendall(write)

    read = sd.recv(BUFFER_SIZE)
    print(f"=> {str(read, 'utf-8').strip()}")

sd.close() # never executed
'''
