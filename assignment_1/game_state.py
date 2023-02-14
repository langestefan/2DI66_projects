import numpy as np
import copy

import assignment_1.constants as c
from assignment_1.board import ChessBoard

import logging

logger = logging.getLogger(__name__)


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
        self.logstr = {"className": self.__class__.__name__}
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

    def set_game_state(self, game_state: c.GameStates) -> None:
        """
        Sets the game state.

        :param game_state: The game state.
        """
        self.game_state = game_state

    def get_board(self) -> ChessBoard:
        """
        Returns the chess board.

        :return: The chess board.
        """
        return self.chess_board

    def game_had_queen_promoted(self) -> bool:
        """
        Returns whether the queen has been promoted.

        :return: True if the queen has been promoted, False otherwise.
        """
        return self.chess_board.game_had_queen_promotion()

    def get_valid_moves(self, player) -> np.ndarray:
        """Checks which moves are valid for the player.

        :param player: The player whose moves are to be checked.
        :param king_in_check: If our king is in check.
        :return: A list of valid moves for the player.
        """
        # collect all possible moves here
        all_moves = self.__get_all_moves(player)
        logger.debug(f"All moves: \n{all_moves}", extra=self.logstr)

        # remove moves that put king in check
        valid_moves = self.__sim_if_moves_put_king_in_check(player, all_moves)

        # filter out invalid moves
        valid_moves = valid_moves[valid_moves[:, 0] != -1]

        return valid_moves

    def king_is_in_check(self, player) -> bool:
        """Checks if the king of the player is in check.

        :param player: The player whose king is to be checked.
        :return: True if the king is in check, False otherwise.
        """
        # get king position
        king_obj = self.get_board().get_king_obj(player)
        king_pos = king_obj.get_position()

        # get opponent pieces
        opponent_pieces = self.get_board().get_all_pieces(
            c.Players(1 - player.value)
        )

        # check if opponent pieces can attack king
        for piece in opponent_pieces:
            moves = piece.get_piece_moves(self.get_board().get_board_arr())

            # check if king pos is in moves
            for move in moves:
                if np.array_equal(move[2:4], king_pos):
                    return True

        # our king is not in check
        return False

    def __get_all_moves(self, player) -> np.ndarray:
        """Returns all possible moves for the player's pieces.

        :param player: The player whose moves are to be checked.
        :return: A list of all possible moves for the player.
        """
        # collect all moves here
        all_moves = np.ones((200, 4), dtype=int) * -1

        # get all pieces of player
        pieces = self.get_board().get_all_pieces(player)

        # get all moves for each piece
        move_idx = 0
        for piece in pieces:
            moves = piece.get_piece_moves(self.get_board().get_board_arr())
            moves_len = len(moves)
            all_moves[move_idx : move_idx + moves_len] = moves
            move_idx += moves_len

        # filter out invalid moves
        all_moves = all_moves[all_moves[:, 0] != -1]

        return all_moves

    def __sim_if_moves_put_king_in_check(self, player, moves) -> np.ndarray:
        # go through all moves
        for idx, move in enumerate(moves):
            if move[0] == -1:
                continue

            # copy the game state (myself)
            gs_cpy = copy.deepcopy(self)
            gs_cpy.current_player = player

            # make the move
            gs_cpy.chess_board.move_piece(
                move[0:2],
                move[2:4],
                player,
                print_info=False,
            )

            # check if the king is in check
            if gs_cpy.king_is_in_check(player):
                # remove the move from the valid moves
                logger.debug(
                    f"Move {move} puts king in check.", extra=self.logstr
                )
                moves[idx] = -1

            # delete the copy
            del gs_cpy

        return moves
