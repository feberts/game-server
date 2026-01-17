"""
Available games.

Every new game must be added to this list.
"""

from games.tictactoe import TicTacToe
from games.yahtzee import Yahtzee
from games.echo import Echo
from games.chat import Chat

games = [TicTacToe, Yahtzee, Echo, Chat]
