#!/usr/bin/env python3

# echo server that handles repeated connections and translates words

def german(word):
    translations = {'cat':'Katze', 'dog':'Hund'}
    word = str(word, 'utf-8').strip()
    ret = translations[word] if word in translations else 'no translation'
    return bytes(ret + '\n', 'utf-8')

import socket

IP = '127.0.0.1'
PORT = 4711
BUFFER_SIZE = 1024

sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sd.bind((IP, PORT))
sd.listen()
print(f'Listening on {IP}:{PORT}')

while True:
    conn, client = sd.accept()
    ip, port = client
    print(f'Accepted connection from {ip}:{port}')

    while True:
        read = conn.recv(BUFFER_SIZE)
        print(f"Received data from {ip}:{port}: {read}")

        if not read:
            conn.close()
            print(f"Closed connection to {ip}:{port}")
            break

        write = german(read)
        print(f"Sending data to {ip}:{port}: {write}")
        conn.sendall(write)

sd.close() # never executed
print('Server shut down')
