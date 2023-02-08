# import numpy as np
import assignment_1.constants as c
import numpy as np


class GameState:
    """
    This class is used to represent the state of the game. It contains the
    round number, the players, who owns which chess pieces, the history of
    moves and decides if the game is over. (comments in reST style.)

    In baby chess there are
     - Two players
     - Each player has 10 pieces:
       (1x king, 1x queen, 1x rooks, 1x bishops, 1x knights, 5x pawns)
     - The board has 5x5
     - Pieces are represented by integers 1-10
     - Players are represented by integers 0 and 1
     - The game is over when one player has no pieces left or when the
       king is captured.


    """

    def __init__(self):
        self.round_number: int = 0
        self.current_player: int = c.PLAYER_WHITE
        self.game_state: int = c.game_states["ongoing"]

    def __str__(self) -> str:
        """
        Returns a string representation of the game state.

        :return: A string representation of the game state.
        """
        return f"Round number: {self.round_number}"

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
        return self.current_player

    def start_new_round(self):
        """
        Starts a new round.
        """
        self.round_number += 1
        self.current_player = (self.current_player + 1) % 2

    def get_game_state(self) -> int:
        """
        Returns the game state.

        :return: The game state.
        """
        return self.game_state

    def __determine_game_state(self, board: np.ndarray) -> int:
        """
        Determines the game state based on the position of the pieces.
        If the game is over, the game state is updated accordingly.

        :return: The game state.
        """
        pass
