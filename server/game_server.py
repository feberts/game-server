#!/usr/bin/env python3
"""
TODO
"""

import config
import json
import socket
import threading
import traceback
import utility
import time # TODO rm after testing

class MessageSizeExceeded(Exception): pass
class ClientDisconnect(Exception): pass

def framework_function(data): # TODO dummy
    return {'status':'ok', 'message':'framework: no such game', 'data':{'player_id':13}}

def request_handler(conn, ip, port):
    """
    TODO
    """
    conn.settimeout(config.TIMEOUT)

    try:
        try:
            # receive data from client:
            request = bytearray()
            
            while True:
                data = conn.recv(config.BUFFER_SIZE)
                request += data
                if not data: break
                if len(request) > config.MESSAGE_SIZE_MAX: raise MessageSizeExceeded
            
            if not len(request): raise ClientDisconnect

            request = str(request, 'utf-8')
            request = json.loads(request)
            print(f'Received {len(request)} bytes from {ip}:{port}')
            print(f'  {request}')

            # pass request to the framework:
            response = framework_function(request)

        except MessageSizeExceeded:
            print(f'Message size exceeded by client {ip}:{port}')
            response = utility.server_error('too much data sent')
        except socket.timeout:
            print(f'Connection timed out {ip}:{port}')
            response = None
        except ClientDisconnect:
            print(f'Disconnect by client {ip}:{port}')
            response = None
        except json.decoder.JSONDecodeError:
            print(f'Corrupt data received from {ip}:{port}')
            response = utility.server_error('received corrupt data')
        except:
            print(f'Unexpected exception:\n' + traceback.format_exc())
            response = utility.server_error('internal error')

        # send response to client:
        if response:
            print(f'Responding to {ip}:{port}: {response}')
            response = json.dumps(response)
            response = bytes(response, 'utf-8')
            conn.sendall(response)

    finally:
        conn.close()
        print(f'Closed connection to {ip}:{port}')

# start server:
try:
    # create listening socket:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sd:
        sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sd.bind((config.IP, config.PORT))
        sd.listen()
        print(f'Listening on {config.IP}:{config.PORT}')

        while True:
            # accept a connection:
            conn, client = sd.accept()
            ip, port = client
            print(f'Accepted connection from {ip}:{port}')

            # handle request in separate thread:
            t = threading.Thread(target=request_handler, args=(conn, ip, port), daemon=True)
            t.start()
except KeyboardInterrupt:
    pass
