"""
Game framework.

This module implements the game framework. The framework is responsible for managing active game sessions. Client requests are parsed, and the appropriate actions are performed. The following requests can be handled by the framework:

- starting a new game
- joining a game
- submitting a move
- requesting the game state
- observing a game
TODO sind weitere neu hinzugekommen?

To perform these actions, the framework calls the corresponding methods of a game class instance.
"""

import time

import config
import games
import game_session
import utility

class GameFramework:
    """
    Class GameFramework.

    This class manages active game sessions and handles the interaction between clients and game instances.
    """

    def __init__(self):
        self._game_classes = games.available_games
        self._game_classes_by_name = {} # game name -> game class
        self._game_sessions = {} # (game name, token) -> game session
        self._build_game_class_dict()

    def _build_game_class_dict(self):
        """
        Build a dictionary mapping game names to game classes.
        """
        for game_class in self._game_classes:
            self._game_classes_by_name[game_class.__name__] = game_class

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

        handlers = {'start_game':self._start_game, 'join_game':self._join_game, 'move':self._move, 'state':self._state, 'watch':self._watch}

        if request['type'] not in handlers:
            return utility.framework_error('invalid request type')

        return handlers[request['type']](request)

    def _start_game(self, request):
        """
        Request handler for starting a game session.

        This function instantiates the requested game and adds it to the list of active game sessions. After the required number of players has joined the game, the function sends the player ID back to the client who requested the start of the game. If not enough players have joined the game before the timeout occurs, the game session is deleted and the requesting client is informed.

        Parameters:
        request (dict): request containing game name, token and number of players

        Returns:
        dict: containing the player ID
        """
        # check and parse request:
        err = utility.check_dict(request, {'game':str, 'token':str, 'players':int, 'name':str})
        if err: return utility.framework_error(err)

        game_name, token, players, name = request['game'], request['token'], request['players'], request['name']

        # get game class:
        if game_name not in self._game_classes_by_name:
            return utility.framework_error('no such game')

        game_class = self._game_classes_by_name[game_name]

        # check number of players:
        if players > game_class.max_players() or players < game_class.min_players():
            return utility.framework_error('invalid number of players')

        # create game session and add it to dictionary of active sessions:
        session = game_session.GameSession(game_class(players), players)
        self._game_sessions[(game_name, token)] = session

        # get player ID:
        player_id = session.next_id(name)

        # wait for others to join:
        self._await_game_start(session)

        if not session.ready(): # timeout reached
            del self._game_sessions[(game_name, token)] # remove game session
            return utility.framework_error('timeout while waiting for others to join')

        self._log_game_sessions()

        return self._return_data({'player_id':player_id, 'request_size_max':config.receive_size_max})

    def _join_game(self, request):
        """
        Request handler for joining a game session.

        This function checks if a game session specified by the game's name and the token is already started and waiting for clients to join. After the required number of players has joined the game, the function sends the player ID back to the client who requested to join the game. If not enough players have joined the game before the timeout occurs, the requesting client is informed.

        Parameters:
        request (dict): request containing game name and token

        Returns:
        dict: containing the player ID
        """
        # check and parse request:
        err = utility.check_dict(request, {'game':str, 'token':str, 'name':str})
        if err: return utility.framework_error(err)

        game_name, token, name = request['game'], request['token'], request['name']

        # retrieve game session:
        session, err = self._retrieve_game_session(game_name, token)
        if err: # no such game or game session
            return err
        if session.ready(): # game is full
            return utility.framework_error('game is already full')

        # get player ID:
        player_id = session.next_id(name)

        # wait for others to join:
        self._await_game_start(session)

        if not session.ready(): # timeout reached
            return utility.framework_error('timeout while waiting for others to join')

        return self._return_data({'player_id':player_id, 'request_size_max':config.receive_size_max})

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

        # retrieve the game:
        session, err = self._retrieve_game_session(game_name, token)
        if err: # no such game or game session
            return err

        game = session.game
        
        # check if game is still active:
        if game.game_over():
            return utility.framework_error('game has ended')

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

        # retrieve the game:
        session, err = self._retrieve_game_session(game_name, token)
        if err: # no such game or game session
            return err

        game = session.game

        # retrieve the game state:
        state = game.state(player_id)

        # add current player's ID and game status:
        state['current'] = game.current_player()
        state['gameover'] = game.game_over()

        return self._return_data(state)

    def _watch(self, request):
        """
        Request handler for observing another player.

        To observe another player in the same game session, the observing client needs to know the ID of that player. This function retrieves that ID based on the player's name. This only works, if the player has supplied a name when joining the game session.

        Parameters:
        request (dict): request containing game name, token and player to be observed

        Returns:
        dict: containing the ID of the observed player
        """
        # check and parse request:
        err = utility.check_dict(request, {'game':str, 'token':str, 'name':str})
        if err: return utility.framework_error(err)

        game_name, token, player_name = request['game'], request['token'], request['name']

        # retrieve game session:
        session, err = self._retrieve_game_session(game_name, token)
        if err: # no such game or game session
            return err
        if not session.ready(): # game has not yet started
            return utility.framework_error('game has not yet started')

        # get player ID:
        player_id, err = session.get_id(player_name)
        if err: return utility.framework_error(err)

        return self._return_data({'player_id':player_id})

    def _await_game_start(self, session):
        """
        Waits for players to join the game.

        This function waits until the required number of players has joined the game or until the timeout is reached.

        Parameters:
        session (GameSession): game session
        """
        seconds = 0
        while not session.ready() and seconds < config.timeout:
            time.sleep(config.game_start_poll_interval)
            seconds = seconds + config.game_start_poll_interval

    def _retrieve_game_session(self, game_name, token):
        """
        Retrieves an active game session.

        If the specified game session exists, it is returned to the caller.

        Parameters:
        game_name (str): game name
        token (str): token

        Returns:
        tuple(GameSession, dict):
            GameSession: game session, None in case of an error
            dict: error message, if a problem occurred, None otherwise
        """
        # check if game session exists:
        if game_name not in self._game_classes_by_name:
            return None, utility.framework_error('no such game')
        if (game_name, token) not in self._game_sessions:
            return None, utility.framework_error('no such game session')

        return self._game_sessions[(game_name, token)], None

    def _return_data(self, data):
        """
        Adds data to a dictionary to be sent back to the client. This function is to be used only for sending regular data back to a client as a response to a valid request. It must not be used for sending error messages (hence the status flag 'ok').
        """
        return {'status':'ok', 'data':data}

    def _log_game_sessions(self):
        """
        Print active games.
        """
        log = 'Game sessions (game:token:players):\n'
        for (game_name, token), session in self._game_sessions.items():
            log += f'{game_name}:{token}:{session._number_of_players}\n'
        print(log)
