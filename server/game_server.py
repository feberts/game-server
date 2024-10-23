#!/usr/bin/env python3
"""
Game server.

This server program opens a port and handles client connections in separate threads. It passes the data received from a client to the game framework and sends the framework's reply back to the client. The connection is then closed. Parameters like IP or port number are defined in the config module.
"""

import config
import json
import socket
import threading
import traceback
import utility

class ClientDisconnect(Exception): pass
class MessageSizeExceeded(Exception): pass

def framework_function(data): # TODO rm dummy
    return {'status':'ok', 'message':'framework: no such game', 'data':{'player_id':13}}

class Logger:
    """
    Logging server output.
    """
    def __init__(self, ip, port):
        self._ip, self._port = ip, port

    def log(self, message, prefix=''):
        print(f'{prefix}[{ip}:{port}] {message}')

def request_handler(conn, ip, port):
    """
    Handling a request.

    This function handles a single request. It
    - receives data from the client
    - passes that data to the framework
    - sends the data returned by the framework back to the client
    - then closes the connection

    Data is expected to be received in JSON format and it is also sent back to the client in JSON format. The connection has a server side timeout and the amount of data accepted in a single request is limited by the server. The corresponding parameters are defined in the config module. Whenever possible, error messages are sent back to the client.

    Parameters:
    conn (socket): connection socket
    client (str): client ip
    port (int): client port
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
            response = framework_function(request) # TODO pass IP and port as well?

        except MessageSizeExceeded:
            l.log('message size exceeded by client')
            response = utility.server_error('too much data sent')
        except socket.timeout:
            l.log('connection timed out on server')
            response = utility.server_error('connection timed out')
        except ClientDisconnect:
            l.log('disconnect by client')
            response = None
        except json.decoder.JSONDecodeError:
            l.log('corrupt data received from client')
            response = utility.server_error('received corrupt data')
        except:
            l.log('unexpected exception on server:\n' + traceback.format_exc())
            response = utility.server_error('internal error')

        # send response to client:
        if response:
            l.log(f'responding to client:\n{response}')
            response = json.dumps(response)
            response = bytes(response, 'utf-8')
            conn.sendall(response)

    finally:
        conn.close()
        l.log('connection closed by server')

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
