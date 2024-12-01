"""
Game server API.

This module provides an API for communicating with the game server. The API can be used to

- start a game that other clients can join
- join a game that was started by another client
- submit moves to the server
- request the game state
- passively observe other players
- reset a game without starting a new session
"""

import json
import socket
import traceback

class GameServerAPI:
    """
    Class GameServerAPI.

    This class provides API functions to communicate with the game server.
    """

    def start_game(self, server, port, game, token, players, name=''):
        """
        Start a game.

        This function asks the server to start a game. Other clients can use the join function to join that game. To be able to join, they need to know the chosen token. The token is used to identify the game session. It can be any string. A repeated call of this function will end the previous session and start a new one, which other players can join.

        The game starts as soon as the specified number of clients has joined the game. The function then returns the player ID. The server assigns IDs in the range 0...players-1 to all players that join the game.

        The optional name parameter makes it possible for other clients to passively observe your playing by joining a game using the watch function. They will be able to retrieve the same game state from the server as you.

        Parameters:
        server (str): server
        port (int): port number
        game (str): name of the game
        token (str): name of the game session
        players (int): total number of players
        name (str): player name (optional)

        Returns:
        tuple(int, str):
            int: player ID, if the game was successfully started, else None
            str: error message, if a problem occurred, None otherwise

        Raises:
        AssertionError: for invalid arguments
        """
        self._process_args(server, port, game, token, name, players)

        response, err = self._send({'type':'start_game', 'game':game, 'token':token, 'players':players, 'name':name})

        if err: return None, err
        self._player_id = response['player_id']
        self._request_size_max = response['request_size_max']

        return self._player_id, None

    def join_game(self, server, port, game, token, name=''):
        """
        Join a game.

        This function lets a client join a game that another client has started by calling the start function. To be able to join, the correct token must be provided. The token is used to identify a specific game session.

        The game starts as soon as all clients have joined the game. The function then returns the player ID. The server assigns IDs in the range 0...players-1 to all players that join the game.

        The optional name parameter makes it possible for other clients to passively observe your playing by joining a game using the watch function. They will be able to retrieve the same game state from the server as you.

        Parameters:
        server (str): server
        port (int): port number
        game (str): name of the game
        token (str): name of the game session
        name (str): player name (optional)

        Returns:
        tuple(int, str):
            int: player ID, if the game could be joined, else None
            str: error message, if a problem occurred, None otherwise

        Raises:
        AssertionError: for invalid arguments
        """
        self._process_args(server, port, game, token, name)

        response, err = self._send({'type':'join_game', 'game':game, 'token':token, 'name':name})

        if err: return None, err
        self._player_id = response['player_id']
        self._request_size_max = response['request_size_max']

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
        if self._player_id == None: return self._api_error('start or join a game first')[1]
        if self._watch_mode: return self._api_error('cannot submit moves in watch mode')[1]

        _, err = self._send({'type':'move', 'game':self._game, 'token':self._token, 'player_id':self._player_id, 'move':kwargs})

        if err: return err

        return None

    def state(self, blocking=True):
        """
        Request the state.

        This function requests the game state from the server. The state is returned as a dictionary. Refer to the documentation of a specific game to find out about the structure and content of the dictionary.

        This function will block until the game state changes. Only then the server will respond with the updated state. This is more efficient than polling. The function can also be used in a non-blocking way. Furthermore, the function does not block, if it is the client's turn to submit a move, or if the game has ended.

        Parameters:
        blocking (bool): use function in blocking mode (default)

        Returns:
        tuple(dict, str):
            dict: game state if state could be retrieved, else None
            str: error message, if a problem occurred, None otherwise
        """
        if self._player_id == None: return self._api_error('start or join a game first')

        state, err = self._send({'type':'state', 'game':self._game, 'token':self._token, 'player_id':self._player_id, 'blocking':blocking, 'observer':self._watch_mode})

        if err: return None, err

        return state, None

    def watch(self, server, port, game, token, name):
        """
        Observe another player.

        This function lets one client observe another client. By providing the name of the player to be observed, you will receive the same data calling the state function as that player does. Moreover, this function will return the player ID of the observed player.

        This function can only be called, after the specified game session has already been started.

        Parameters:
        server (str): server
        port (int): port number
        game (str): name of the game
        token (str): name of the game session
        name (str): name of player to observe

        Returns:
        tuple(int, str):
            int: ID of observed player, None in case of an error
            str: error message, if a problem occurred, None otherwise

        Raises:
        AssertionError: for invalid arguments
        """
        self._process_args(server, port, game, token, name)
        assert name != '', 'Invalid argument: name'

        response, err = self._send({'type':'watch', 'game':game, 'token':token, 'name':name})

        if err: return None, err
        self._player_id = response['player_id']
        self._watch_mode = True

        return self._player_id, None

    def reset_game(self):
        """
        Reset a game.

        This function resets the current game. There is no need to rejoin the game, and all players will keep their IDs. This is useful when simulating many games to collect data for AI training. Only the client who started the game can reset it.

        Returns:
        str: error message, if game could not be reset, None otherwise
        """
        if self._player_id != 0: return self._api_error('game can only be reset by starter')[1]

        _, err = self._send({'type':'reset_game', 'game':self._game, 'token':self._token, 'player_id':self._player_id})

        if err: return err

        return None

    def _send(self, data):
        """
        Send data to the server and receive its response.

        This function sends data to the server and returns the data sent back by it. The data is sent in JSON format. Make sure, that the passed dictionary's content is compatible with JSON. Before sending data, this function checks if the request exceeds the size limit. A default value for that limit is defined by this class. It is updated with a value transmitted by the server after starting or joining a game.

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

    def _process_args(self, server, port, game, token, name, players=1):
        """
        Check arguments and assign them to class attributes.
        """
        def msg(msg): return 'Invalid argument: ' + msg

        assert type(server) == str and len(server) > 0, msg('server')
        assert type(port) == int and port >= 0 and port <= 65535, msg('port')
        assert type(game) == str and len(game) > 0, msg('game')
        assert type(token) == str and len(token) > 0, msg('token')
        assert type(players) == int and players > 0, msg('players')
        assert type(name) == str, msg('name')

        self._server = server
        self._port = port
        self._game = game
        self._token = token

    class _MissingResponse(Exception): pass

    def __init__(self):
        # game session:
        self._game = None
        self._token = None
        self._player_id = None
        self._watch_mode = False

        # server:
        self._server = None
        self._port = None

        # connections:
        self._buffer_size = 4096 # bytes
        self._request_size_max = int(1e6) # bytes (updated after starting/joining a game)
