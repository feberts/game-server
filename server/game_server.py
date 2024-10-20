#!/usr/bin/env python3
"""
TODO
"""

import json
import socket
import threading
import traceback

IP = '127.0.0.1'
PORT = 4711

class ClientDisconnect(Exception): pass


def framework_function(data): # TODO dummy
    return {'status':'ok', 'message':'framework: no such game', 'data':{'player_id':13}}

def request_handler(conn):
    try:
        # receive data from client:
        request = bytearray()
        
        while True:
            data = conn.recv(4096)
            if not data: raise ClientDisconnect
            request += data
            if request[-5:] == b'_EOF_': break
        
        # prepare data:
        request = request[:-5] # strip EOF
        request = str(request, 'utf-8')
        request = json.loads(request)
        print(f"Received from {ip}:{port}: {request}")

        # pass request to the framework:
        response = framework_function(request)

        # send response to client:
        print(f"Responding to {ip}:{port}: {response}")
        response = json.dumps(response)
        conn.sendall(bytes(response, 'utf-8'))

    except ClientDisconnect:
        print(f"Client disconnected {ip}:{port}")
    except:
        print('Unexpected exception >>>>>')
        print(traceback.format_exc())
        print('<<<<< Unexpected exception')
    finally:
        conn.close()
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

            # handle request in seperate thread:
            t = threading.Thread(target=request_handler, args=(conn,), daemon=True)
            t.start()
except KeyboardInterrupt:
    pass
