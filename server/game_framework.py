"""
Game framework.

This module implements the game framework. The framework is responsible for managing active games. It serves as an intermediary between the server and active game instances.

Client requests are parsed and the appropriate actions are performed. The following list shows the types of requests the framework can handle and the resulting actions:

- start_game: instantiating game class objects
- join_game: assigning clients to games
- move: forwarding player moves to game instances
- state: reporting the game state to clients

To perform these actions, the framework calls the corresponding methods of a game class instance, if necessary.
"""
# TODO spell check of this whole file

import threading
import time

import config
import utility

from tictactoe import TicTacToe

class GameFramework:
    """
    Class GameFramework.

    This class manages active games and handles the interaction between clients and game instances.
    """

    def __init__(self):
        self._game_classes = [TicTacToe] # list of available games
        self._game_classes_by_name = {} # game name -> game class
        self._active_games = {} # (game name, token) -> active game
        self._build_game_class_dict()

    def _build_game_class_dict(self):
        """
        Build a dictionary mapping game names to game classes.
        """
        for game in self._game_classes:
            self._game_classes_by_name[game.__name__] = game

    def handle_request(self, request):
        """
        Handling a client request.

        This function is called by the server. It identifies the type of the request and redirects it to the corresponding method. The returned data is handed back to the server and then sent to the client.

        Parameters:
        request (dict): client request

        Returns:
        dict: reply
        """
        if 'type' not in request:
            return utility.framework_error("key 'type' of type str missing")

        handlers = {'start_game':self._start_game, 'join_game':self._join_game} # TODO add more handlers

        if request['type'] not in handlers:
            return utility.framework_error('invalid request type')

        return handlers[request['type']](request)

    class _ActiveGame:
        """
        Wrapper class for game instances providing functionality for retrieving player IDs.
        """
        def __init__(self, game_instance, players):
            self.game = game_instance
            self._number_of_players = players
            self._next_id = 0
            self._lock = threading.Lock()

        def get_id(self):
            with self._lock:
                ret = self._next_id
                self._next_id = self._next_id + 1
                return ret

        def ready(self):
            # ready when all players have joined the game
            return self._number_of_players == self._next_id

    def _start_game(self, request):
        """
        Request handler for starting a game.
        
        This function instantiates the requested game and adds it to the list of active games. This function is blocking. After the required number of players has joined the game, the function sends the player ID back to the client who requested the start of the game. If not enough players have joined the game before the timeout occurs, the game instance is deleted and the requesting client is informed accordingly.

        Parameters:
        request (dict): request containing game name, token and number of players

        Returns:
        dict: containing the player ID
        """
        # check and parse request:
        err = utility.check_dict(request, {'game':str, 'token':str, 'players':int})
        if err: return utility.framework_error(err)

        game_name, token, players = request['game'], request['token'], request['players']

        # get game class:
        if game_name not in self._game_classes_by_name:
            return utility.framework_error('no such game')

        game_class = self._game_classes_by_name[game_name]

        # check number of players:
        if players > game_class.max_players() or players < game_class.min_players():
            return utility.framework_error('invalid number of players')

        # create game instance and add it to dictionary of active games:
        new_game = self._ActiveGame(game_class(players), players)
        self._active_games[(game_name, token)] = new_game

        # get player ID:
        player_id = new_game.get_id()

        # wait for others to join:
        self._await_game_start(new_game)

        if not new_game.ready(): # timeout reached
            del self._active_games[(game_name, token)]
            return utility.framework_error('timeout while waiting for others to join')

        return self._return_data({'player_id':player_id})

    def _retrieve_active_game(self, game, token):
        """
        Retrieves an active game.
        
        If the specified game session exists, it is returned to the caller.

        Parameters:
        game (str): game name
        token (str): token

        Returns:
        _ActiveGame: active game specified by game name and token
        """
        # check if game session exists:
        if game not in self._game_classes_by_name:
            return None, utility.framework_error('no such game')
        if (game, token) not in self._active_games:
            return None, utility.framework_error('no such game session')

        return self._active_games[(game, token)], None

    def _await_game_start(self, game):
        """
        Waits for players to join the game.
        
        This function waits until the required number of players has joined the game or until the timeout is reached.
        
        Parameters:
        game (_ActiveGame): game instance
        """
        seconds = 0
        while not game.ready() and seconds < config.timeout:
            time.sleep(config.game_start_poll_interval)
            seconds = seconds + config.game_start_poll_interval

    def _join_game(self, request):
        """
        Request handler for joining a game.
        
        This function checks if a game specified by its name and token is already started and waiting for clients to join. This function is blocking. After the required number of players has joined the game, the function sends the player ID back to the client who requested to join the game. If not enough players have joined the game before the timeout occurs, the requesting client is informed accordingly.

        Parameters:
        request (dict): request containing game name and token

        Returns:
        dict: containing the player ID
        """
        # check and parse request:
        err = utility.check_dict(request, {'game':str, 'token':str})
        if err: return utility.framework_error(err)

        game_name, token = request['game'], request['token']

        # retrieve game:
        game, err = self._retrieve_active_game(game_name, token)
        if err:
            return err # no such game or game session
        if game.ready():
            return utility.framework_error('game is already full')

        # get player ID:
        player_id = game.get_id()

        # wait for others to join:
        self._await_game_start(game)

        if not game.ready(): # timeout reached
            return utility.framework_error('timeout while waiting for others to join')

        return self._return_data({'player_id':player_id})

    def _return_data(self, data):
        """
        Adds data to a dictionary to be sent back to the client. This function is to be used only for sending regular data back to a client as a response to a valid request. It must not be used for sending error messages (hence the status flag 'ok').
        """
        return {'status':'ok', 'data':data}
