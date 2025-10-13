"""
Server configuration.

This file contains configuration data for the server and framework.
"""

# server:
ip = '127.0.0.1'
port = 4711

# tcp connections:
receive_size_max = int(1e6) # bytes, prevents clients from sending too much data
buffer_size = 4096 # bytes
connection_timeout = 60 # seconds

# framework:
game_timeout = 180 # timeout for inactive games and for joining a game

# logging:
log_server_info = False # useful only for debugging tcp connections (verbose)
log_server_errors = True # errors during tcp connections
log_framework_info = True # actions performed by the framework
log_framework_request = True # client requests
log_framework_response = True # server responses
