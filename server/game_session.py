"""
Game session.

This module provides a class that handles a single game session.
"""

import copy
import random
import string
import threading
import time

class GameSession:
    """
    Class GameSession.

    This class contains a game instance and all data associated with the
    specific game session. It assigns player IDs, passes requests like player
    moves to the game instance, and provides the framework with information
    about the game session.
    """

    def __init__(self, game_class, players):
        """
        Constructor.

        Instantiating a game class object and initializing other attributes.

        Parameters:
        game_class (class AbstractGame): the game class itself (not an instance of it)
        players (int): number of players
        """
        self._game_class = game_class
        self._n_players = players
        self._game = game_class(players)
        self._next_id = 0
        self._player_ids = {} # player name -> ID
        self._passwords = {} # player ID -> password
        self._last_access = time.time()
        self._lock = threading.Lock()
        self._state_change = threading.Event()
        self._previous_game = None # previous game instance stored upon reset
        self._previous_game_ids = [] # players will receive state of previous game once

    def next_id(self, player_name):
        """
        Returning a player ID and a password.

        This function returns a new ID and a password for each player joining a
        game session. If a none empty string is passed as the player name, this
        name together with the assigned ID is added to a dictionary.

        Parameters:
        player_name (str): player name, can be an empty string

        Returns:
        int: the next player ID
        str: a generated password
        """
        with self._lock:
            # player ID:
            player_id = self._next_id
            self._next_id += 1

            # associate player name with ID:
            if player_name != '':
                self._player_ids[player_name] = player_id

            # generate password:
            password = self._password()
            self._passwords[player_id] = password

            return player_id, password

    def ready(self):
        """
        Game session is ready to start as soon as all players have joined the
        game.

        Returns:
        bool: True, if session ready
        """
        return self._n_players == self._next_id

    def get_id(self, player_name):
        """
        Return player ID and password by name.

        This function returns the ID and password that were assigned to the
        player.

        Parameters:
        player_name (str): name of a player that has already joined the game

        Returns:
        tuple(int, str, str):
            int: player ID, None if no such player exists
            str: password, None if no such player exists
            str: error message, if a problem occurred, None otherwise
        """
        if not player_name in self._player_ids:
            return None, None, 'no such player'

        player_id = self._player_ids[player_name]

        return player_id, self._passwords[player_id], None

    def get_game(self, player_id=None):
        """
        Return the game instance.

        Parameters:
        player_id (int): player ID

        Returns:
        AbstractGame: game instance
        """
        if player_id in self._previous_game_ids:
            return self._previous_game

        return self._game

    def last_access(self):
        """
        Return time of last access.
        """
        return self._last_access

    def _update_last_access(self):
        """
        Update time of last access.
        """
        self._last_access = time.time()

    def game_move(self, move, player_id):
        """
        Pass player's move to the game instance.

        When this function is called, an event is triggered to wake up other
        threads waiting for the game state to change.

        Parameters:
        move (dict): the player's move
        player_id (int): ID of the player submitting the move

        Returns:
        str: error message in case the move was illegal, None otherwise (see AbstractGame.move)
        """
        with self._lock:
            ret = self._game.move(move, player_id)
            self._update_last_access()
            self._state_change.set()
            return ret

    def game_state(self, player_id, blocking, observer):
        """
        Retrieve the game state from the game instance.

        If the corresponding API function is called in blocking mode, then this
        thread's execution is paused until the game state changes. To achieve
        this, the thread that changes the state triggers an event to wake up
        other threads waiting for that event. This function does not block, if
        it is the client's turn to submit a move, or if the game has ended.

        If the game has been reset by some client, then for a single time the
        state of the previous game is returned to each client. This is necessary
        for a client to be able to detect the end of the previous game. See
        function reset_game for details.

        Parameters:
        player_id (int): player ID
        blocking (bool): if True, API function was called in blocking mode
        observer (bool): if True, client requesting the state is a passive observer

        Returns:
        dict: game state
        """
        # wait for game state to change:
        if (blocking
            and not self._game.game_over()
            and not (player_id in self._game.current_player() and not observer)
            and not player_id in self._previous_game_ids):
            self._state_change.clear()
            self._state_change.wait()

        # if required, return the previous game's state:
        if player_id in self._previous_game_ids:
            ret = self._previous_game.state(player_id)
            self._previous_game_ids.remove(player_id)
            return ret

        # return current game's state:
        with self._lock:
            self._update_last_access()
            return self._game.state(player_id)

    def reset_game(self):
        """
        Reset the game.

        The game instance is replaced with a new one. The old instance is
        stored. This is necessary to allow the other clients to detect the end
        of the previous game. Otherwise, they would suddenly find themselves in
        a new game without being notified about it. To achieve this, a list of
        client IDs is created upon resetting a game. When a client then calls
        the state function, the state of the previous game is returned a single
        time, and the client's ID is removed from the list. From then on, the
        client will receive the game state of the new game instance.

        Only the client who started the game can reset it.
        """
        # store old game instance and a list of player IDs:
        if self._game.game_over():
            self._previous_game_ids = list(range(1, self._n_players))
            self._previous_game = copy.deepcopy(self._game)

        # create new game instance:
        self._game = self._game_class(self._n_players)

        # wake up other threads waiting for the game state to change:
        self._state_change.set()

    def _password(self, length=5):
        """
        Generate a unique password.

        Parameters:
        length (int): length of the password

        Returns:
        str: the password
        """
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def password_valid(self, player_id, password):
        """
        Check if password and player ID match.

        Parameters:
        player_id (int): player ID
        password (str): password

        Returns:
        bool: True, if password valid
        """
        return player_id in self._passwords and self._passwords[player_id] == password
