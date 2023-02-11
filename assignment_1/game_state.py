import numpy as np

import assignment_1.constants as c
from assignment_1.board import ChessBoard


class GameState:
    """
    This class is used to represent the state of the game.

    It contains the round number, the players, who owns which chess pieces,
    the history of moves and decides if the game is over. (docs in reST style)

    In baby chess there are
     - Two players
     - Each player has 10 pieces:
       (1x king, 1x queen, 1x rooks, 1x bishops, 1x knights, 5x pawns)
     - The board has 5x5
     - Pieces are represented by integers 1-10
     - Players are represented by integers 0 and 1
     - The game is over when one player has no pieces left or when the
       king is captured.

    Attributes:
        round_number (int): The round number of the game.
        current_player (Players): The player who is currently playing.
        game_state (GameStates): The game state. Ongoing, draw or won.
        chess_board (ChessBoard): The chess board. NxN ndarray.
    """

    def __init__(self):
        self.round_number: int = -1  # Call start_new_round() to increment to 0
        self.current_player: c.Players = c.Players.WHITE  # White starts
        self.game_state: c.GameStates = c.GameStates.ONGOING
        self.chess_board: ChessBoard = ChessBoard(init_pieces=True)

    def __str__(self) -> str:
        return f"Round number: {self.round_number}"

    def get_round_number(self) -> int:
        """
        Returns the round number of the game.

        :return: The round number of the game.
        """
        return self.round_number

    def get_current_player(self) -> c.Players:
        """
        Returns the player who is currently playing.

        :return: The player who is currently playing.
        """
        return self.current_player

    def increment_round_number(self) -> None:
        """
        Increments the round number.
        """
        # start new round, increment round number and set current player
        self.round_number += 1
        self.current_player = c.Players(self.round_number % 2)

    def start_new_round(self, move: np.ndarray) -> None:
        """
        Starts a new round.

        :param move: Move to be made.
        """
        if move.shape == (1, 4):
            move = move.squeeze()
        if move.shape != (4,):
            raise ValueError("Move must be a 4 element array.")

        print(
            f"Round {self.round_number} started. Now playing:"
            f" {self.current_player}"
        )
        print(f"Move: {move}")

        # make move
        old_pos = move[0:2]
        new_pos = move[2:4]
        self.chess_board.move_piece(old_pos, new_pos, self.current_player)

    def get_game_state(self) -> c.GameStates:
        """
        Returns the game state.

        :return: The game state.
        """
        return self.game_state

    def get_board(self) -> ChessBoard:
        """
        Returns the chess board.

        :return: The chess board.
        """
        return self.chess_board
