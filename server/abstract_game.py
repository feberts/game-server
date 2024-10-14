"""
This module provides a base class for games.
"""

class AbstractGame:
    """
    Base class for games.

    This class serves as an abstract base class for games. Every new game must be derived from this class and implement all its methods. These methods will be called by the framework. Furthermore, every new game must be added to the list of available games. See the documentation for details on how to add new games.

    None of the methods may raise exceptions. Instead, flags and error messages must be returned to respond to invalid arguments. The flags and messages are then sent back to the client, where they are returned from an API function. So make sure to return meaningful messages.

    In some cases, the framework performs checks before it calls a method. In such a case, you can assume, that the argument passed is valid. Refer to the method descriptions to see which parameters this may apply to.
    """

    def __init__(self, players):
        """
        Constructor.

        The framework assigns IDs in the range 0..n to all players that join a game. It then passes the total number of players to the constructor.

        Parameters:
        players (int): number of players (no parameter check needed)
        """
        raise NotImplementedError

#    def min_players(self):
#        """
#        Returns the minimal number of players.
#
#        This function reports the minimal number of players required to play the game to the framework.
#
#        Returns:
#        int: minimal number of players
#        """
#        raise NotImplementedError
#
#    def max_players(self):
#        """
#        Returns the maximal number of players.
#
#        This function reports the maximal number of players allowed in the game to the framework.
#
#        Returns:
#        int: maximal number of players
#        """
#        raise NotImplementedError
#
#    def current_player(self):
#        """
#        Returns the current player's ID.
#
#        This class must keep track of which player must perform the next move. This function reports this player's ID to the framework. The framework makes sure, that no other player can submit a move.
#
#        Returns:
#        int: current players ID
#        """
#        raise NotImplementedError
#
#    def move(self, move):
#        """
#        Submit a move.
#
#        A player's move is passed as a dictionary. The content of this dictionary entirely depends on the needs of the game. The API function to submit a move on the client side accepts the data as keyword arguments. Those keyword arguments are then converted to a dictionary.
#
#        It is important to let the user of the API know about the names of these keywords and their data types. See the documentation on how to add new games for more details.
#
#        The framework makes sure, that only the current player can submit a move.
#
#        Parameters:
#        move (dict): the current players move
#
#        Returns:
#        tuple(bool, str):
#            bool: to inform the client whether the move was valid or not
#            str: error message in case the move was illegal, an empty string otherwise
#        """
#        raise NotImplementedError
#
#    def state(self, player_id):
#        """
#        Returns the game state as a dictionary.
#
#        This can be the complete state of the game, or just specific information for a specific player. What information is returned depends entirely on the game. In some games all information is available to all players, in other games players can possess information that is hidden from the others.
#
#        It is important to let the user of the API know how the dictionary is structured so he can access its content. See the documentation on how to add new games for more details.
#
#        Parameters:
#        player_id (int): player ID (no parameter check needed)
#
#        Returns:
#        dict: game state
#        """
#        raise NotImplementedError
