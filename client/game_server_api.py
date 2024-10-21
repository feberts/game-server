"""
Game server API.

This module provides an API for communicating with the game server. The API can be used to

- start a game that other clients can join
- join a game that was started by another client
- submit moves to the server
- request the game state
"""

import json
import socket

class GameServerAPI:
    """
    Class GameServerAPI.

    This class provides API functions to communicate with the game server.
    """

    def start_game(self, server, port, game, players, token):
        """
        Start a game.

        This function asks the server to start a game. Other clients can use the join-function to join that game. To be able to join, they need to know the chosen token. The token is used, to identify the game session. It can be any string. A repeated call of this function with the same values for 'game' and 'token' will end the previous session.

        This is a blocking function. The game starts as soon as the specified number of clients has joined the game. The function then returns the player ID. The server assigns IDs in the range 0..players-1 to all players that join the game.

        Parameters:
        server (str): server IP
        port (int): port number
        game (str): name of the game
        players (int): total number of players
        token (str): name of the game session

        Returns:
        tuple(int, str):
            int: player ID, if the game was successfully started, else None
            str: error message, if a problem occurred, an empty string otherwise
        """
        assert type(server) == str and len(server) > 0
        assert type(port) == int and port >= 0
        assert type(game) == str and len(game) > 0
        assert type(players) == int and players > 0
        assert type(token) == str and len(token) > 0

        self._server = server
        self._port = port
        self._game = game
        self._players = players
        self._token = token

        response, msg = self._send({'request':'join', 'game':game, 'players':players, 'token':token})
        
        if not response: return None, msg
        
        self._player_id = response['player_id']
        return self._player_id, ''

    def _send(self, data):
        """
        Send data to server and receive a response.

        This function sends data to the server and returns the data sent back by the server. The data is sent in JSON format. Make sure, that the passed dictionary's content is compatible with JSON.

        Parameters:
        data (dict): data to be sent to the server

        Returns:
        tuple(dict, str):
            dict: data returned by server, None in case of an error
            str: error message, if a problem occurred, an empty string otherwise
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sd:
            try:
                # connect to server:
                sd.settimeout(1.0)
                sd.connect((self._server, self._port))
            except:
                return None, f'api: unable to connect to {self._server}:{self._port}'

            try:
                # send data to server:
                request = json.dumps(data)
                request = bytes(request, 'utf-8')
                sd.sendall(request)
                sd.shutdown(socket.SHUT_WR)

                # receive data from server:
                response = bytearray()
                while True:
                    data = sd.recv(4096)
                    if not data: break
                    response += data
                response = str(response, 'utf-8')
                response = json.loads(response)

                if response['status'] == 'error': # server responded with error
                    return None, response['message']
                return response['data'], ''
            except socket.timeout:
                return None, 'api: connection timed out'
            except:
                return None, 'api: communication with server failed'

    _server = None
    _port = None
    _game = None
    _players = None
    _token = None
    _player_id = None
