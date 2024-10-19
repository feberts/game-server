#!/usr/bin/env python3
"""
TODO
"""

import json
import socket
import time # TODO weg
import threading

IP = '127.0.0.1'
PORT = 4711
BUFFER_SIZE = 1024

def request_handler(conn):
    with conn:
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
        #conn.close() # TODO weg
        #time.sleep(5) # TODO weg
        print(f"Closed connection to {ip}:{port}")

try:
    # open listening socket:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sd:
        sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sd.bind((IP, PORT))
        sd.listen()
        print(f'Listening on {IP}:{PORT}')

        while True:
            # accept a connection:
            conn, client = sd.accept()
            ip, port = client
            print(f'Accepted connection from {ip}:{port}')

            t = threading.Thread(target=request_handler, args=(conn,), daemon=True)
            t.start()
            #request_handler(conn)
            #with conn:
                ## receive data from client:
                #read = conn.recv(BUFFER_SIZE)
                #read = str(read, 'utf-8')
                #read = json.loads(read)
                #print(f"Received data from {ip}:{port}: {read}")

                ## send data to client:
                #reply = {'Vom Sever':456}
                #state = json.dumps(reply)
                #conn.sendall(bytes(state, 'utf-8'))
                ##time.sleep(1000) # TODO weg

                ## close connection:
                ##conn.close() # TODO weg
                #print(f"Closed connection to {ip}:{port}")

except KeyboardInterrupt:
    pass

print('\nServer shut down')
