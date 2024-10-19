#!/usr/bin/env python3
"""
TODO
"""

import json
import socket

IP = '127.0.0.1'
PORT = 4711
BUFFER_SIZE = 1024

try:
    # open listening socket:
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sd.bind((IP, PORT))
    sd.listen()
    print(f'Listening on {IP}:{PORT}')

    while True:
        # accept a connection:
        conn, client = sd.accept()
        ip, port = client
        print(f'Accepted connection from {ip}:{port}')

        # receive data from client:
        read = conn.recv(BUFFER_SIZE)
        read = str(read, 'utf-8')
        read = json.loads(read)
        print(f"Received data from {ip}:{port}: {read}")

        # send data to client:
        reply = {'Vom Sever':456}
        state = json.dumps(reply)
        conn.sendall(bytes(state, 'utf-8'))

        # close connection:
        conn.close()
        print(f"Closed connection to {ip}:{port}")

except KeyboardInterrupt:
    try: conn.close()
    except: pass
finally:
    sd.close()
    print('\nServer shut down')
