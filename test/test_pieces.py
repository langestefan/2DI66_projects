import assignment_1.constants as c
from assignment_1.pieces import Pawn, Rook, Knight, Bishop, Queen, King

import pytest


class TestClientPieces:
    @pytest.fixture(autouse=True)
    def create_pieces(self):
        """
        Creates a piece object.
        """
        return (
            Pawn(c.Players.WHITE),
            Rook(c.Players.WHITE),
            Knight(c.Players.WHITE),
            Bishop(c.Players.WHITE),
            Queen(c.Players.WHITE),
            King(c.Players.WHITE),
        )

    def test_piece_creation(self, create_pieces):
        """
        Tests if the piece object is created correctly.
        """
        for piece in create_pieces:
            assert piece is not None
            assert piece.player == c.Players.WHITE
            assert piece.name is not None
