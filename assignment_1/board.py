import assignment_1.constants as c
import assignment_1.pieces as p
import numpy as np

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


class ChessBoard:
    """
    This class is used to manage a chess board.
    """

    def __init__(self):
        # Initialize the board with initial positions.
        self.board = self.__create_initial_board(c.PIECES)

    def __str__(self):
        """Returns a string representation of the board."""
        s = ""
        for i in range(c.BOARD_SIZE):
            for j in range(c.BOARD_SIZE):
                if self.board[i][j] is None:
                    s += " ."
                else:
                    symbol = f" {self.board[i][j].symbol}"
                    if self.board[i][j].player is c.Players.WHITE:
                        symbol = c.bcolors.OKBLUE + symbol + c.bcolors.ENDC
                    else:
                        symbol = c.bcolors.FAIL + symbol + c.bcolors.ENDC
                    s += symbol

            s += "\n"
        return "\n" + s

    def __copy__(self):
        return ChessBoard()

    def __create_initial_board(self, pieces: dict):
        """
        Creates a board with the pieces in their initial positions.

        :param pieces: A dictionary containing the pieces and their positions.
        :return: A BOARD_SIZExBOARD_SIZE numpy array representing the board.
        """
        board = np.ndarray((c.BOARD_SIZE, c.BOARD_SIZE), dtype=p.Piece)

        # Initialize the board with empty squares.
        for i in range(c.BOARD_SIZE):
            for j in range(c.BOARD_SIZE):
                board[i][j] = None

        # Add the white pieces to the board.
        white_pieces = pieces["White"]
        for piece in white_pieces.values():
            if piece["player"] is not c.Players.WHITE:
                raise ValueError("Invalid player.")
            piece_obj = self.__return_piece_obj(piece)
            # print(type(piece_obj))
            board[piece["pos"][0]][piece["pos"][1]] = piece_obj

        # Add the black pieces to the board.
        black_pieces = pieces["Black"]
        for piece in black_pieces.values():
            if piece["player"] is not c.Players.BLACK:
                raise ValueError("Invalid player.")
            piece_obj = self.__return_piece_obj(piece)
            board[piece["pos"][0]][piece["pos"][1]] = piece_obj

        return board

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

    def get_board(self) -> np.ndarray:
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

    def get_valid_moves(self, player: c.Players) -> list:
        """
        Returns a list of valid moves for a given player.
        :param player: The player whose valid moves are being retrieved.
        :return: A list of valid moves.
        """
        moves = []
        for piece in self.get_all_pieces(player):
            moves.extend(
                piece.__determine_valid_moves__(self.board, piece, player)
            )
        return moves

    def __determine_valid_moves(
        self, piece: p.Piece, player: c.Players
    ) -> list:
        moves = []
        return moves

    def get_piece(self, pos: np.ndarray) -> p.Piece:
        """
        Returns a piece at a given position.
        :param row: The row of the piece.
        :param col: The column of the piece.
        :return: A piece.
        """
        piece = self.board[pos[0]][pos[1]]
        return piece  # type: ignore
