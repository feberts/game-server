"""
Available games.

Every new game must be added to this list.
"""

from games.tictactoe import TicTacToe
from games.yahtzee import Yahtzee
from games.echo import Echo

games = [TicTacToe, Yahtzee, Echo]
