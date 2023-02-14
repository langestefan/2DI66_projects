import numpy as np
from typing import Type, TypeVar

import assignment_1.constants as c
import assignment_1.pieces as p

import logging

logger = logging.getLogger(__name__)


# Classic baby chess board representation:
#   -------------
# 5 | k q b n r | Black
# 4 | p p p p p |
# 3 | . . . . . |
# 2 | P P P P P |
# 1 | R N B Q K | White
#   -------------
#     a b c d e

# Encoded representation of the chess board:
#   -------------
# 0 | k q b n r | Black
# 1 | p p p p p |
# 2 | . . . . . |
# 3 | P P P P P |
# 4 | R N B Q K | White
#   -------------
#     0 1 2 3 4

# Represented as a BOARD_SIZExBOARD_SIZE numpy array:
# 0 [[k q b n r ]  |
# 1 [ p p p p p ]  |
# 2 [ . . . . . ]  | Rows
# 3 [ P P P P P ]  |
# 4 [ R N B Q K ]] |
#     0 1 2 3 4
#      Columns
# Where white pieces are uppercase and black pieces are lowercase.

TPieces = TypeVar("TPieces", bound=p.Piece)


class ChessBoard:
    """
    This class is used to manage a chess board.
    """

    def __init__(self, init_pieces: bool = True):
        self.logstr = {"className": self.__class__.__name__}

        # Create the board with initial positions.
        self.board = np.ndarray((c.BOARD_SIZE, c.BOARD_SIZE), dtype=p.Piece)
        if init_pieces:
            self.__create_initial_board(c.PIECES)

    def __str__(self):
        """Returns a string representation of the board."""
        s = ""
        for i in range(c.BOARD_SIZE):
            s += f"{i} "
            for j in range(c.BOARD_SIZE):
                if self.board[i][j] is None:
                    s += " ."
                else:
                    symbol = f" {self.board[i][j].symbol}"
                    if self.board[i][j].player is c.Players.WHITE:
                        symbol = c.bcolors.OKBLUE + symbol
                    else:
                        symbol = c.bcolors.FAIL + symbol

                    s += symbol + c.bcolors.ENDC

            s += "\n"
        s += "   0 1 2 3 4"

        return "\n" + s

    def __copy__(self):
        board_cpy = self.board.copy()
        return board_cpy

    def put_new_piece_on_board(
        self,
        piece: p.Piece,
        position: np.ndarray,
        overwrite: bool = False,
        ignore_pos_check: bool = False,
        do_consistency_check: bool = False,
    ):
        """
        Put a new piece on the board.

        :param piece: The piece to create.
        :param position: The position to set the piece on.
        :param overwrite: If True, overwrite the piece on the position.
        :param ignore_pos_check: Ignore check if piece is already on this pos.
        :return: Updated board with the piece on the new position.
        """
        # check if the position is None
        if self.board[position[0]][position[1]] is not None and not overwrite:
            raise ValueError(
                "Invalid position, already a piece here and overwrite is"
                " False."
            )

        self.board[position[0]][position[1]] = piece
        piece.set_position(position, ignore_pos_check=ignore_pos_check)

        if do_consistency_check:
            if not self.__board_consistency_check():
                raise ValueError(
                    "Board positions are not consistent with piece positions."
                )

    def __board_consistency_check(self):
        """
        Checks if the board is consistent.

        :return: True if the board is consistent, False otherwise.
        """
        for i in range(c.BOARD_SIZE):
            for j in range(c.BOARD_SIZE):
                if self.board[i][j] is not None:
                    if not np.array_equal(self.board[i][j].position, [i, j]):
                        return False

        return True

    def __create_initial_board(self, pieces: dict):
        """
        Creates a board with the pieces in their initial positions.

        :param pieces: A dictionary containing the pieces and their positions.
        :return: A BOARD_SIZExBOARD_SIZE numpy array representing the board.
        """

        # Initialize the board with empty squares.
        for i in range(c.BOARD_SIZE):
            for j in range(c.BOARD_SIZE):
                self.board[i][j] = None

        # add pieces to the board
        for player in pieces.keys():
            for piece in pieces[player].values():
                if piece["player"] is not player:
                    raise ValueError("Invalid player.")
                piece_obj = self.__return_piece_obj(piece)

                # update the position on the board and the piece object
                self.put_new_piece_on_board(
                    piece=piece_obj,
                    position=piece["pos"],
                    do_consistency_check=True,
                )

    def __return_piece_obj(self, piece: dict):
        """
        Returns a piece object based on the piece dictionary.

        :param piece: A dictionary containing the piece information.
        :return: A piece object.
        """
        piece_type = piece["type"]
        player = piece["player"]

        if piece_type == c.ChessPieceTypes.KING:
            return p.King(player)
        elif piece_type == c.ChessPieceTypes.KNIGHT:
            return p.Knight(player)
        elif piece_type == c.ChessPieceTypes.ROOK:
            return p.Rook(player)
        elif piece_type == c.ChessPieceTypes.BISHOP:
            return p.Bishop(player)
        elif piece_type == c.ChessPieceTypes.QUEEN:
            return p.Queen(player)
        elif piece_type == c.ChessPieceTypes.PAWN:
            return p.Pawn(player)
        else:
            raise ValueError("Invalid piece type.")

    def get_board_arr(self) -> np.ndarray:
        """
        Returns a copy of the board.
        :return: The board.
        """
        board_cpy = self.board.copy()
        return board_cpy

    def get_all_pieces(self, player: c.Players) -> list:
        """
        Returns a unordered list of pieces for a given player.
        :param player: The player whose pieces are being retrieved.
        :return: A list of pieces.
        """
        pieces = []
        for i in range(c.BOARD_SIZE):
            for j in range(c.BOARD_SIZE):
                if (
                    self.board[i][j] is not None
                    and self.board[i][j].get_player() == player
                ):
                    pieces.append(self.board[i][j])
        return pieces

    def get_piece(self, pos: np.ndarray) -> p.Piece:
        """
        Returns a piece at a given position.
        :param row: The row of the piece.
        :param col: The column of the piece.
        :return: A piece.
        """
        pos = pos.squeeze()
        piece = self.board[pos[0]][pos[1]]
        return piece  # type: ignore

    def get_king_obj(self, player: c.Players) -> p.King:
        """
        Returns the king object for a given player.
        :param player: The player whose king is being retrieved.
        :return: A king.
        """
        for i in range(c.BOARD_SIZE):
            for j in range(c.BOARD_SIZE):
                if (
                    self.board[i][j] is not None
                    and self.board[i][j].get_player() == player
                    and type(self.board[i][j]) == p.King
                ):
                    return self.board[i][j]

    def get_piece_loc_by_type(
        self, piece_type: Type[TPieces], player: c.Players
    ) -> np.ndarray:
        """
        Returns the location of a piece of a given type for a given player.
        :param piece_type: The type of the piece.
        :param player: The player whose piece is being retrieved.
        :return: A piece.
        """
        piece_locs = np.ones((10, 2), dtype=int) * -1

        idx: int = 0
        for i in range(c.BOARD_SIZE):
            for j in range(c.BOARD_SIZE):
                if (
                    self.board[i][j] is not None
                    and self.board[i][j].get_player() == player
                    and type(self.board[i][j]) == piece_type
                ):
                    piece_locs[idx] = [i, j]
                    idx += 1

        # if idx == 0, then we didn't find any pieces of the given type
        if idx == 0:
            raise ValueError("No pieces of the given type found.")

        # remove the empty rows
        piece_locs = piece_locs[piece_locs != -1].reshape(-1, 2)
        return piece_locs

    def move_piece(
        self,
        old_pos: np.ndarray,
        new_pos: np.ndarray,
        player: c.Players,
        set_old_pos_to_none: bool = True,
        print_info: bool = True,
    ):
        """
        Moves a piece from one position to another. Note that we only do a
        few sanity checks here to make sure the move is valid.

        :param old_pos: Old position of the piece.
        :param new_pos: New position of the piece.
        :param player: Player whose piece is being moved.
        :param set_old_pos_to_none: If True, the old position will be set to None.
        :param print_info: If True, info will be printed after the move.
        :return: True if we captured a piece, False otherwise.
        """
        piece = self.board[old_pos[0]][old_pos[1]]
        new_pos_cont = self.board[new_pos[0]][new_pos[1]]

        # check if the new position is on the board
        if new_pos[0] < 0 or new_pos[0] >= c.BOARD_SIZE:
            raise ValueError("Invalid position, row out of bounds.")
        if new_pos[1] < 0 or new_pos[1] >= c.BOARD_SIZE:
            raise ValueError("Invalid position, column out of bounds.")

        # check if the old position is None
        if piece is None:
            raise ValueError("Invalid position, no piece here.")

        # check if the piece belongs to the player
        if piece.get_player() != player:  # type: ignore
            raise ValueError("Invalid player.")

        # check if new pos is None, check if the piece is the same color
        if new_pos_cont is not None:
            if new_pos_cont.get_player() == player:  # type: ignore
                logger.error(
                    "Invalid move, same color piece here.", extra=self.logstr
                )
                raise ValueError("Invalid move, same color piece here.")

            logger.debug(f"Player {player} captured the piece: {new_pos_cont.name}", extra=self.logstr)  # type: ignore

        # check if it's the first move for the pawn
        if type(piece) == p.Pawn:  # type: ignore
            if piece.is_first_move():  # type: ignore
                piece.set_first_move_false()  # type: ignore

            elif np.abs(new_pos[0] - old_pos[0]) > 1:
                raise ValueError(
                    "Invalid move, pawn can only move 2 spaces on first move."
                )

        # check if the move switches columns
        if new_pos[1] != old_pos[1]:
            if piece.get_column_switch() is False:  # type: ignore
                raise ValueError("Invalid move, piece cannot switch columns.")
            else:
                piece.increment_column_switch_count()  # type: ignore

        # update the board, move the piece
        # change pawn to queen in case of promotion
        if piece.name == "Pawn" and new_pos[0] % 4 == 0:
            piece_obj = p.Queen(piece.player)
            self.put_new_piece_on_board(piece_obj, new_pos, overwrite=True)

        else:
            self.board[new_pos[0]][new_pos[1]] = piece
            piece.set_position(new_pos)  # type: ignore

        if set_old_pos_to_none:
            self.board[old_pos[0]][old_pos[1]] = None

        # only for debugging
        if print_info:
            logger.debug(self, extra=self.logstr)
