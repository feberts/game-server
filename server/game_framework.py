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

    class _ActiveGame:
        """
        Wrapper class for game instances providing functionality for retrieving player IDs.
        """
        def __init__(self, game_instance, players):
            self.game = game_instance
            self._number_of_players = players
            self._next_id = 0
            self._lock = threading.Lock()

        def next_id(self): # IDs assigned to clients joining the game
            with self._lock:
                ret = self._next_id
                self._next_id = self._next_id + 1
                return ret

        def ready(self): # ready when all players have joined the game
            return self._number_of_players == self._next_id

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

        handlers = {'start_game':self._start_game, 'join_game':self._join_game, 'move':self._move, 'state':self._state}

        if request['type'] not in handlers:
            return utility.framework_error('invalid request type')

        return handlers[request['type']](request)

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
        player_id = new_game.next_id()

        # wait for others to join:
        self._await_game_start(new_game)

        if not new_game.ready(): # timeout reached
            del self._active_games[(game_name, token)] # remove game
            return utility.framework_error('timeout while waiting for others to join')

        self._log_active_games()

        return self._return_data({'player_id':player_id})

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
        if err: # no such game or game session
            return err
        if game.ready(): # game is full
            return utility.framework_error('game is already full')

        # get player ID:
        player_id = game.next_id()

        # wait for others to join:
        self._await_game_start(game)

        if not game.ready(): # timeout reached
            return utility.framework_error('timeout while waiting for others to join')

        return self._return_data({'player_id':player_id})

    def _move(self, request):
        """
        Request handler for player moves.

        This function handles a client's move. It makes sure, that it is actually the client's turn to submit a move. It then passes the move to the game instance and returns the game instance's message in case of an invalid move.

        Parameters:
        request (dict): containing information about the game session and the player's move

        Returns:
        dict: containing an error message, if the move is invalid
        """
        # check and parse request:
        err = utility.check_dict(request, {'game':str, 'token':str, 'player_id':int, 'move':dict})
        if err: return utility.framework_error(err)

        game_name, token, player_id, move = request['game'], request['token'], request['player_id'], request['move']

        # retrieve game:
        active_game, err = self._retrieve_active_game(game_name, token)
        if err: # no such game or game session
            return err

        game = active_game.game

        # check if it is the client's turn:
        if game.current_player() != player_id:
            return utility.framework_error('not your turn')

        # pass the move to the game instance:
        err = game.move(move)
        if err: return utility.game_error(err)

        return self._return_data(None)

    def _state(self, request):
        """
        Request handler for game state requests.

        This function retrieves the game state from a game instance and sends it back to the client. It calls the game instance's state function and passes the player ID.

        Parameters:
        request (dict): containing information about the game session and the player

        Returns:
        dict: containing the game state
        """
        # check and parse request:
        err = utility.check_dict(request, {'game':str, 'token':str, 'player_id':int})
        if err: return utility.framework_error(err)

        game_name, token, player_id = request['game'], request['token'], request['player_id']

        # retrieve game:
        active_game, err = self._retrieve_active_game(game_name, token)
        if err: # no such game or game session
            return err

        game = active_game.game

        # retrieve the game state from the game instance:
        state = game.state(player_id)

        return self._return_data(state)

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

    def _retrieve_active_game(self, game, token):
        """
        Retrieves an active game.

        If the specified game session exists, it is returned to the caller.

        Parameters:
        game (str): game name
        token (str): token

        Returns:
        tuple(_ActiveGame, dict):
            _ActiveGame: active game specified by name and token, None in case of an error
            dict: error message, if a problem occurred, None otherwise
        """
        # check if game session exists:
        if game not in self._game_classes_by_name:
            return None, utility.framework_error('no such game')
        if (game, token) not in self._active_games:
            return None, utility.framework_error('no such game session')

        return self._active_games[(game, token)], None

    def _return_data(self, data):
        """
        Adds data to a dictionary to be sent back to the client. This function is to be used only for sending regular data back to a client as a response to a valid request. It must not be used for sending error messages (hence the status flag 'ok').
        """
        return {'status':'ok', 'data':data}

    def _log_active_games(self):
        """
        Print active games.
        """
        log = 'GAME                TOKEN               PLAYERS\n'
        for session, instance in self._active_games.items():
            game, token = session
            log += f'{game:20}{token:20}{instance._number_of_players:7}\n'
        print(log)
