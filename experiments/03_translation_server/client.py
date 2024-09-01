#!/usr/bin/env python3

# client that sends words to the server and receives translations

import socket

IP = '127.0.0.1'
PORT = 4711
BUFFER_SIZE = 1024

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
