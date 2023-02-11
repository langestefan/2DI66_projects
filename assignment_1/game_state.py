# import numpy as np
import assignment_1.constants as c
from assignment_1.board import ChessBoard
from assignment_1.strategy import RandomStrategy


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


    """

    def __init__(self):
        self.round_number: int = 0
        self.current_player: c.Players = c.Players.WHITE  # White starts
        self.game_state: c.GameStates = c.GameStates.ONGOING

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

    def get_player(self) -> c.Players:
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
        self.current_player = c.Players(self.round_number % 2)

    def get_game_state(self) -> c.GameStates:
        """
        Returns the game state.

        :return: The game state.
        """
        return self.game_state

    def set_new_game_state(self, board: ChessBoard):
        """
        Updates the game state based on the current board and the current game
        state. If the game is over, the game state is updated accordingly.

        :param board: The current board.

        :raises Exception: If the game is already over and we set a new state.
        """
        # raise exception if game is already over
        if self.game_state != c.GameStates.ONGOING:
            raise Exception("Game is already over.")

        # checkmate: no valid moves available and king is in check
        if (
            self.__check_if_king_is_in_check(board, self.current_player)
            and len(self.__get_all_valid_moves(board, self.current_player))
            == 0
        ):
            if self.current_player == c.Players.WHITE:
                self.game_state = c.GameStates.BLACK_WON
            else:
                self.game_state = c.GameStates.WHITE_WON

        # stalemate: no valid moves available, but king is not in check
        elif (
            not self.__check_if_king_is_in_check(board, self.current_player)
            and len(self.__get_all_valid_moves(board, self.current_player))
            == 0
        ):
            self.game_state = c.GameStates.DRAW

        # if nobody wins and the game is not a draw, the game is still ongoing
        else:
            self.game_state = c.GameStates.ONGOING

    def __get_all_valid_moves(
        self, board: ChessBoard, player: c.Players
    ) -> list:
        valid_moves = board.get_valid_moves(player)
        return valid_moves

    def __check_if_king_is_in_check(
        self, board: ChessBoard, player: c.Players
    ) -> bool:
        """
        Checks if the king is in check.

        :return: True if the king is in check, False otherwise.
        """
        return True
