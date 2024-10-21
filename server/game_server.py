#!/usr/bin/env python3
"""
TODO
"""

import json
import socket
import threading
import traceback
import utility

IP = '127.0.0.1'
PORT = 4711

class ClientDisconnect(Exception): pass
class DataSizeExceeded(Exception): pass


def framework_function(data): # TODO dummy
    return {'status':'ok', 'message':'framework: no such game', 'data':{'player_id':13}}

def request_handler(conn, ip, port):
    try:
        try:
            # receive data from client:
            request = bytearray()
            
            while True:
                data = conn.recv(4096)
                if not data: raise ClientDisconnect
                request += data
                if len(request) > 1e6: raise DataSizeExceeded
                if request[-5:] == b'_EOF_': break
            
            # prepare data:
            request = request[:-5] # strip EOF
            request = str(request, 'utf-8')
            request = json.loads(request)
            print(f'Received from {ip}:{port}: {request}')

            # pass request to the framework:
            response = framework_function(request)

        except DataSizeExceeded:
            print(f'Data size exceeded by client {ip}:{port}')
            response = utility.error_msg('too much data sent')
        except ClientDisconnect:
            raise ClientDisconnect
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
