"""
Game session.

This module provides a class that contains all data associated with a specific game session.
"""

import copy
import threading
import time

class GameSession:
    """
    Class GameSession.

    This is a wrapper class for game instances providing additional functionality.
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
        self._player_names = {} # player name -> ID
        self._last_access = time.time()
        self._lock = threading.Lock()
        self._state_change = threading.Event()
        self._previous_game = None # stored upon reset
        self._previous_ids = [] # will receive the status of the previous game once

    def next_id(self, player_name):
        """
        Returning a player ID.

        This function returns a new ID for each player joining a game session. If a none empty string is passed as the player name, this name together with the assigned ID are added to a dictionary.

        Parameters:
        player_name (str): player name, can be an empty string

        Returns:
        int: the next player ID
        """
        with self._lock:
            # player ID:
            player_id = self._next_id
            self._next_id += 1

            # associate player name with ID:
            if player_name != '':
                self._player_names[player_name] = player_id

            return player_id

    def ready(self):
        """
        Game session is ready to start as soon as all players have joined the game.

        Returns:
        bool: True, if session ready, else False
        """
        return self._n_players == self._next_id

    def get_id(self, player_name):
        """
        Return player ID by name.

        This function returns the ID that was assigned to the player.

        Parameters:
        player_name (str): name of an existing player that has already joined the game

        Returns:
        tuple(int, str):
            int: player ID, None if no such player exists
            str: error message, if a problem occurred, None otherwise
        """
        if not player_name in self._player_names:
            return None, 'no such player'

        return self._player_names[player_name], None

    def get_game(self, player_id=None):
        """
        Return the game instance.

        Parameters:
        player_id (int): player ID

        Returns:
        AbstractGame: game instance
        """
        if player_id in self._previous_ids:
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

        When this function is called, an event is triggered to wake up other threads waiting for the game state to change.

        Parameters:
        move (dict): the player's move
        player_id (int): ID of the player submitting the move

        Returns:
        str: error message in case the move was illegal, None otherwise
        """
        with self._lock:
            ret = self._game.move(move, player_id)
            self._update_last_access()
            self._state_change.set()
            return ret

    def game_state(self, player_id, blocking, observer):
        """
        Retrieve the game state from the game instance.

        If the corresponding API function is called in blocking mode, then this thread's execution is paused until the game state changes. To achieve this, the thread that changes the state triggers an event to wake up other threads waiting for that event. This function does not block, if it is the client's turn to submit a move, or if the game has ended.

        If the game has been reset by some client, then for a single time the state of the previous game is returned to each client. This is necessary for a client to be able to detect the end of the previous game. See function reset_game for details.

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
            and not player_id in self._previous_ids):
            self._state_change.clear()
            self._state_change.wait()

        # if required, return the previous game's state:
        if player_id in self._previous_ids:
            ret = self._previous_game.state(player_id)
            self._previous_ids.remove(player_id)
            return ret

        # return current game's state:
        with self._lock:
            self._update_last_access()
            return self._game.state(player_id)

    def reset_game(self):
        """
        Reset the game.

        The game instance is replaced with a new one. The old instance is stored. This is necessary to allow the other clients to detect the end of the previous game. Otherwise, they would suddenly find themselves in a new game without being notified about it. To achieve this, a list of client IDs is created upon resetting a game. When a client then calls the state function, the old game state is returned a single time. Then the client is removed from the list. After that, he will receive the game state of the new game instance.

        Only the client who started the game can reset it.
        """
        # store old game instance and a list of player IDs:
        if self._game.game_over():
            self._previous_ids = [player_id for player_id in range(1, self._n_players)]
            self._previous_game = copy.deepcopy(self._game)

        # wake up other threads waiting for the game state to change:
        self._state_change.set()

        # create new game instance:
        self._game = self._game_class(self._n_players)
