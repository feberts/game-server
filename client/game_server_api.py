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
import traceback

class GameServerAPI:
    """
    Class GameServerAPI.

    This class provides API functions to communicate with the game server.
    """

    def start_game(self, server, port, game, token, players):
        """
        Start a game.

        This function asks the server to start a game. Other clients can use the join-function to join that game. To be able to join, they need to know the chosen token. The token is used to identify the game session. It can be any string. A repeated call of this function will end the previous session.

        TODO blockierend nicht möglich, wenn _send() mit Timeout arbeitet !!!
        This is a blocking function. The game starts as soon as the specified number of clients has joined the game. The function then returns the player ID. The server assigns IDs in the range 0..players-1 to all players that join the game.

        Parameters:
        server (str): server
        port (int): port number
        game (str): name of the game
        token (str): name of the game session
        players (int): total number of players

        Returns:
        tuple(int, str):
            int: player ID, if the game was successfully started, else None
            str: error message, if a problem occurred, an empty string otherwise

        Raises:
        AssertionError: for invalid arguments
        """
        self._process_args(server, port, game, token, players)

        response, err = self._send({'request':'start', 'game':game, 'token':token, 'players':players})

        if not response: return None, err
        self._player_id = response['player_id']

        return self._player_id, ''

    def _send(self, data):
        """
        Sends data to the server and receive its response.

        This function sends data to the server and returns the data sent back by it. The data is sent in JSON format. Make sure, that the passed dictionary's content is compatible with JSON.

        Parameters:
        data (dict): data to be sent to the server

        Returns:
        tuple(dict, str):
            dict: data returned by server, None in case of an error
            str: error message, if a problem occurred, an empty string otherwise
        """
        # prepare data:
        try:
            request = json.dumps(data)
            request = bytes(request, 'utf-8')
        except:
            return self._api_error('data could not be converted to JSON')

        if len(request) > self._message_size_max:
            return self._api_error('message size exceeded')

        # create a socket:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sd:
            try:
                # connect to server:
                sd.settimeout(self._timeout) # TODO entfernen, damit Funktion blockierend genutzt werden kann ???
                sd.connect((self._server, self._port))
            except:
                return self._api_error(f'unable to connect to {self._server}:{self._port}')

            try:
                # send data to server:
                sd.sendall(request)
                sd.shutdown(socket.SHUT_WR) # signal end of message

                # receive data from server:
                response = bytearray()

                while True:
                    data = sd.recv(self._buffer_size)
                    if not data: break
                    response += data

                if not response: raise self.MissingResponse
                response = str(response, 'utf-8')
                response = json.loads(response)

                # return data:
                if response['status'] == 'error': # server responded with error
                    return None, response['message']

                return response['data'], ''

            except socket.timeout:
                return self._api_error('connection timed out')
            except self.MissingResponse:
                return self._api_error('empty or no response received from server')
            except (ConnectionResetError, BrokenPipeError):
                return self._api_error('connection closed by server')
            except json.decoder.JSONDecodeError:
                return self._api_error('received corrupt data')
            except:
                return self._api_error('unexpected exception:\n' + traceback.format_exc())

    def _api_error(self, message):
        return None, 'api: ' + message

    def _process_args(self, server, port, game, token, players=1):
        """
        Check arguments and assign them to class attributes.
        """
        def msg(msg): return 'Invalid argument: ' + msg

        assert type(server) == str and len(server) > 0, msg('server')
        assert type(port) == int and port >= 0 and port <= 65535, msg('port')
        assert type(game) == str and len(game) > 0, msg('game')
        assert type(token) == str and len(token) > 0, msg('token')
        assert type(players) == int and players > 0, msg('players')

        self._server = server
        self._port = port
        self._game = game
        self._token = token
        self._players = players

    class MissingResponse(Exception): pass

    def __init__(self):
        # game:
        self._game = None
        self._players = None
        self._token = None
        self._player_id = None

        # server:
        self._server = None
        self._port = None

        # connections:
        self._buffer_size = 4096 # bytes
        self._timeout = 5 # seconds
        self._message_size_max = 1000 # bytes
