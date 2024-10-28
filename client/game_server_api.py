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

        This function asks the server to start a game. Other clients can use the join function to join that game. To be able to join, they need to know the chosen token. The token is used to identify the game session. It can be any string. A repeated call of this function will end the previous session.

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
            str: error message, if a problem occurred, None otherwise

        Raises:
        AssertionError: for invalid arguments
        """
        self._process_args(server, port, game, token, players)

        response, err = self._send({'type':'start_game', 'game':game, 'token':token, 'players':players})

        if err: return None, err
        self._player_id = response['player_id']

        return self._player_id, None

    def join_game(self, server, port, game, token):
        """
        Join a game.

        This function lets a client join a game that another client has started by calling the start function. To be able to join, the correct token must be provided. The token is used to identify a specific game session.

        This is a blocking function. The game starts as soon as all clients have joined the game. The function then returns the player ID. The server assigns IDs in the range 0..players-1 to all players that join the game.

        Parameters:
        server (str): server
        port (int): port number
        game (str): name of the game
        token (str): name of the game session

        Returns:
        tuple(int, str):
            int: player ID, if the game could be joined, else None
            str: error message, if a problem occurred, None otherwise

        Raises:
        AssertionError: for invalid arguments
        """
        self._process_args(server, port, game, token)

        response, err = self._send({'type':'join_game', 'game':game, 'token':token})

        if err: return None, err
        self._player_id = response['player_id']

        return self._player_id, None

    def move(self, **kwargs):
        """
        Submit a move.

        This function is used to submit a move to the game server. The move must be passed as keyword arguments. Refer to the documentation of a specific game to find out about the required or available arguments. If it is not your turn to submit a move or if the move is invalid, the server replies with an error message.

        Parameters:
        kwargs (dict): player move as keyword arguments

        Returns:
        str: error message, if a problem occurred, None otherwise
        """
        _, err = self._send({'type':'move', 'game':self._game, 'token':self._token, 'player_id':self._player_id, 'move':kwargs})

        if err: return err

        return None

    def state(self):
        """
        Request the state.

        This function requests the game state from the server. The state is returned as a dictionary. Refer to the documentation of a specific game to find out about the structure and content of that dictionary.
    
        Returns:
        tuple(dict, str):
            dict: game state if state could be retrieved, else None
            str: error message, if a problem occurred, None otherwise
        """
        response, err = self._send({'type':'state', 'game':self._game, 'token':self._token, 'player_id':self._player_id})
        if err: return None, err

        state = response['data']

        return state, None

    def _send(self, data):
        """
        Send data to the server and receive its response.

        This function sends data to the server and returns the data sent back by it. The data is sent in JSON format. Make sure, that the passed dictionary's content is compatible with JSON.

        Parameters:
        data (dict): data to be sent to the server

        Returns:
        tuple(dict, str):
            dict: data returned by server, None in case of an error
            str: error message, if a problem occurred, None otherwise
        """
        # prepare data:
        try:
            request = json.dumps(data)
            request = bytes(request, 'utf-8')
        except:
            return self._api_error('data could not be converted to JSON')

        if len(request) > self._request_size_max:
            return self._api_error('message size exceeded')

        # create a socket:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sd:
            try:
                # connect to server:
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

                if not response: raise self._MissingResponse
                response = str(response, 'utf-8')
                response = json.loads(response)

                # return data:
                if response['status'] == 'error': # server responded with error
                    return None, response['message']

                return response['data'], None

            except socket.timeout:
                return self._api_error('connection timed out')
            except self._MissingResponse:
                return self._api_error('empty or no response received from server')
            except (ConnectionResetError, BrokenPipeError):
                return self._api_error('connection closed by server')
            except json.decoder.JSONDecodeError:
                return self._api_error('received corrupt data')
            except:
                return self._api_error('unexpected exception:\n' + traceback.format_exc())

    def _api_error(self, message):
        """
        Return an error message.
        """
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

    class _MissingResponse(Exception): pass

    def __init__(self):
        # game:
        self._game = None
        self._token = None
        self._players = None
        self._player_id = None

        # server:
        self._server = None
        self._port = None

        # connections:
        self._buffer_size = 4096 # bytes
        self._request_size_max = int(1e6) # bytes
