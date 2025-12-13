"""
Server configuration.

This file contains configuration data for the server and framework.
"""

# SERVER:
ip = '127.0.0.1'
port = 4711

# FRAMEWORK:
game_timeout = 1000 # seconds, timeout for inactive games and for joining a game

# LOGGING:
log_server_info = False # useful for debugging tcp connections (verbose)
log_server_errors = True # errors during tcp connections
log_framework_request = True # client requests
log_framework_response = True # server responses
log_framework_actions = True # actions performed by the framework, such as terminating games

# TCP CONNECTIONS:
# pick a higher value for request_size_max if required by a new game;
# it should not be necessary to change buffer_size or connection_timeout
request_size_max = int(1e6) # bytes, prevents clients from sending too much data
buffer_size = 4096 # bytes, corresponds to client-side buffer size value
connection_timeout = 60 # seconds, timeout for tcp transactions
