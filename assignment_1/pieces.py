from abc import ABC, abstractmethod
import numpy as np

import assignment_1.constants as c


class Piece(ABC):
    """A base class to represent a piece on a chess board

    :param player: The player who owns the piece.
    """

    def __init__(self, player: c.Players):
        self.player = player  # The player who owns the piece.
        self.name = "Piece"  # This is just a placeholder name.
        self.position: np.ndarray = np.array(
            [0, 0], dtype=int
        )  # The position of the piece on the board.
        self.valid_moves: list = []  # A list of valid moves for the piece.

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
        if position == self.position:
            raise ValueError("Piece is already on this position.")
        self.position = position


class Pawn(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "Pawn"
        self.symbol = "P"


class Rook(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "Rook"
        self.symbol = "R"


class Knight(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "Knight"
        self.symbol = "N"


class Bishop(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "Bishop"
        self.symbol = "B"


class Queen(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "Queen"
        self.symbol = "Q"


class King(Piece):
    def __init__(self, player: c.Players):
        super().__init__(player)
        self.name = "King"
        self.symbol = "K"
