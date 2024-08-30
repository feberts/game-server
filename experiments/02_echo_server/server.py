#!/usr/bin/env python3

# server for hello world with sockets
# taken from this turorial: https://realpython.com/python-sockets/

import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, # address family: IPv4
                   socket.SOCK_STREAM # socket type: TCP
                   ) as s: # no need to call s.close()
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept() # blocking
    # addr: address of client, tuple (host, port)
    # conn: NEW socket object representing the connection (distinct from the listening socket that the server is using to accept new connections)
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024) # blocking, reads whatever data the client sends
            if not data:
                # If conn.recv() returns an empty bytes object, b'', that signals that the client closed the connection
                break
            conn.sendall(data)
