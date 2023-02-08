import numpy as np


class GameState:
    """
    This class is used to represent the state of the game. It contains the round number,
    the players, who owns which chess pieces, the history of moves and decides if the
    game is over. (comments in reST style.)

    In baby chess there are
     - Two players
     - Each player has 10 pieces:
       (1x king, 1x queen, 1x rooks, 1x bishops, 1x knights, 5x pawns)
     - The board has 5x5
     - Pieces are represented by integers 1-10
     - Players are represented by integers 0 and 1

    :param round_number: The round number of the game.


    """

    n_players = 2
    n_pieces = 10

    def __init__(self):
        self.round_number: int = 0

    def get_round_number(self) -> int:
        """
        Returns the round number of the game.

        :return: The round number of the game.
        """
        return self.round_number

    def get_player(self) -> int:
        """
        Returns the player who is currently playing.

        :return: The player who is currently playing.
        """
        return self.round_number % self.n_players
