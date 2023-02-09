from abc import ABC, abstractmethod
import numpy as np

import assignment_1.constants as c


class Piece(ABC):
    """A base class to represent a piece on a chess board

    :param player: The player who owns the piece.
    """

    def __init__(self, player: c.Players):
        self.player = player  # The player who owns the piece.
        self.name = "Piece"  # Placeholder name for debug, should not be used.
        self.position: np.ndarray = np.array(
            [-1, -1], dtype=int
        )  # The position of the piece on the board.
        self.n_moves: int = 0  # The number of moves the piece can at max make.

    def __str__(self):
        return f"{self.name} owned by player {self.player}"

    def get_player(self) -> c.Players:
        """
        Returns the player who owns the piece.

        :return: The player who owns the piece.
        """
        return self.player

    def get_position(self) -> np.ndarray:
        """
        Returns the position of the piece on the board.

        :return: Position encoded as a [x, y] numpy array.
        """
        return self.position

    def set_position(self, position: np.ndarray):
        """
        Sets the position of the piece on the board.

        :param position: Position encoded as a [x, y] numpy array.
        """
        for i in position:
            if i < 0 or i > c.BOARD_SIZE - 1:
                raise ValueError("Position is not on the board.")
        if (position == self.position).all():
            raise ValueError("Piece is already on this position.")
        self.position = position

    @abstractmethod
    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        """
        Returns a list of valid moves for the piece.

        :param board: The current board state.
        :return: A list of valid moves for the piece.
        """
        pass


class Pawn(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "Pawn"
        self.symbol = "P"

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        valid_moves = np.ones((1, 4), dtype=int) * -1
        return valid_moves


class Rook(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "Rook"
        self.symbol = "R"

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        valid_moves = np.ones((1, 4), dtype=int) * -1
        return valid_moves


class Knight(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "Knight"
        self.symbol = "N"

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        valid_moves = np.ones((1, 4), dtype=int) * -1
        return valid_moves


class Bishop(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "Bishop"
        self.symbol = "B"

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        valid_moves = np.ones((1, 4), dtype=int) * -1
        return valid_moves


class Queen(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "Queen"
        self.symbol = "Q"

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        valid_moves = np.ones((1, 4), dtype=int) * -1
        return valid_moves


class King(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "King"
        self.symbol = "K"
        # the king can go up, left, right, and diagonally 1 square = 5 moves
        self.n_moves = 5

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        move_candidates = np.ones((self.n_moves, 4), dtype=int) * -1
        valid_moves = np.ones((self.n_moves, 4), dtype=int) * -1

        # write old position of this piece to valid_moves
        old_loc = [self.position]
        move_candidates[:, 0:2] = np.repeat(old_loc, 5, axis=0)

        # get coordinates of move candidates
        x = old_loc[0][0]
        y = old_loc[0][1]

        if self.player == c.Players.WHITE:  # white
            new_x = np.transpose([[x] * 2 + [x - 1] * 3])
        else:  # black
            new_x = np.transpose([[x] * 2 + [x + 1] * 3])
        new_y = np.transpose([[y - 1, y + 1, y - 1, y, y + 1]])

        move_candidates[:, 2:4] = np.concatenate((new_x, new_y), axis=1)

        # TODO: check which move candidates are valid and filter them out

        return valid_moves
