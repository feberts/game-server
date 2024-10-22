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

class ClientDisconnect(Exception): pass
class MessageSizeExceeded(Exception): pass

def framework_function(data): # TODO rm dummy
    return {'status':'ok', 'message':'framework: no such game', 'data':{'player_id':13}}
    
class Logger:
    """
    Logging.
    """
    def __init__(self, ip, port):
        self._ip, self._port = ip, port
    def log(self, message, prefix=''):
        print(f'{prefix}[{ip}:{port}] {message}')

def request_handler(conn, ip, port):
    """
    TODO
    """
    conn.settimeout(config.timeout)
    l = Logger(ip, port)

    try:
        try:
            # receive data from client:
            request = bytearray()
            
            while True:
                data = conn.recv(config.buffer_size)
                request += data
                if not data: break
                if len(request) > config.message_size_max:
                    raise MessageSizeExceeded
            
            if not len(request): raise ClientDisconnect

            l.log(f'received {len(request)} bytes from client')
            request = str(request, 'utf-8')
            request = json.loads(request)
            l.log(f'received from client:\n{request}')

            # pass request to the framework:
            response = framework_function(request)

        except MessageSizeExceeded:
            l.log(f'message size exceeded by client')
            response = utility.server_error('too much data sent')
        except socket.timeout:
            l.log(f'connection timed out on server')
            response = None
        except ClientDisconnect:
            l.log(f'disconnect by client')
            response = None
        except json.decoder.JSONDecodeError:
            l.log(f'corrupt data received from client')
            response = utility.server_error('received corrupt data')
        except:
            l.log(f'unexpected exception on server:\n' + traceback.format_exc())
            response = utility.server_error('internal error')

        # send response to client:
        if response:
            l.log(f'responding to client:\n{response}')
            response = json.dumps(response)
            response = bytes(response, 'utf-8')
            conn.sendall(response)

    finally:
        conn.close()
        l.log(f'connection closed by server')

# start server:
try:
    # create listening socket:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sd:
        sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sd.bind((config.ip, config.port))
        sd.listen()
        print(f'Listening on {config.ip}:{config.port}')

        while True:
            # accept a connection:
            conn, client = sd.accept()
            ip, port = client
            Logger(ip, port).log('connection accepted', '\n')

            # handle request in separate thread:
            t = threading.Thread(target=request_handler, args=(conn, ip, port), daemon=True)
            t.start()
except KeyboardInterrupt:
    pass
