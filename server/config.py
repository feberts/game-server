"""
Server configuration.

This file contains configuration data for the server and framework.
"""

# SERVER:
ip = '127.0.0.1'
port = 4711

# FRAMEWORK:
game_timeout = 180 # seconds, timeout for inactive games and for joining a game

# LOGGING:
log_server_info = False # useful only for debugging tcp connections (verbose)
log_server_errors = True # errors during tcp connections
log_framework_info = True # actions performed by the framework
log_framework_request = True # client requests
log_framework_response = True # server responses

# TCP CONNECTIONS:
request_size_max = int(1e6) # bytes, prevents clients from sending too much data
buffer_size = 4096 # bytes, corresponds to client-side buffer size value
connection_timeout = 60 # seconds, timeout for tcp connections

# it should not be necessary to change buffer_size or connection_timeout;
# pick a higher value for request_size_max if required by a new game
