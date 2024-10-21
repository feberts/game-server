#!/usr/bin/env python3
"""
TODO
"""

import json
import socket
import threading
import traceback
import utility
import time

IP = '127.0.0.1'
PORT = 4711

class MessageSizeExceeded(Exception): pass


def framework_function(data): # TODO dummy
    #time.sleep(3)
    return {'status':'ok', 'message':'framework: no such game', 'data':{'player_id':13}}

def request_handler(conn, ip, port):
    try:
        try:
            # receive data from client:
            request = bytearray()
            
            while True:
                data = conn.recv(4096)
                request += data
                if not data: break
                if len(request) > 1e6: raise MessageSizeExceeded
            
            # prepare data:
            request = str(request, 'utf-8')
            request = json.loads(request)
            print(f'Received from {ip}:{port}: {request}')

            # pass request to the framework:
            response = framework_function(request)

        except MessageSizeExceeded:
            print(f'Message size exceeded by client {ip}:{port}')
            response = utility.error_msg('too much data sent')
        except json.decoder.JSONDecodeError:
            print(f'Corrupt data received from {ip}:{port}')
            response = utility.error_msg('received corrupt json data')
        except:
            print(f'Unexpected exception:')
            print(traceback.format_exc())
            response = utility.error_msg('internal server error')
        
        # send response to client:
        print(f'Responding to {ip}:{port}: {response}')
        response = json.dumps(response)
        conn.sendall(bytes(response, 'utf-8'))

    except ClientDisconnect:
        print(f'Disconnect by client {ip}:{port}')
    finally:
        conn.close()
        print(f'Closed connection to {ip}:{port}')

try:
    # create listening socket:
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
            t = threading.Thread(target=request_handler, args=(conn, ip, port), daemon=True)
            t.start()
except KeyboardInterrupt:
    pass
