import pytest
import numpy as np

import assignment_1.constants as c
from assignment_1.board import ChessBoard
from assignment_1.pieces import Pawn, Rook, Knight, Bishop, Queen, King


class TestClientGameState:
    @pytest.fixture(autouse=True)
    def create_board(self):
        """
        Creates a chess board object
        """
        return ChessBoard()

    def test_board_creation(self, create_board):
        """
        Tests if the board is created correctly.
        """
        assert create_board is not None
        assert create_board.get_board() is not None
        assert create_board.get_board().shape == (c.BOARD_SIZE, c.BOARD_SIZE)

    def test_board_get_piece(self, create_board):
        """
        Tests if the correct piece is retrieved.
        """
        assert create_board.get_piece([0, 0]) is not None
        assert create_board.get_piece([0, 0]).name == "King"
        assert create_board.get_piece([0, 0]).player == c.Players.BLACK
        assert create_board.get_piece([4, 4]) is not None
        assert create_board.get_piece([4, 4]).name == "King"
        assert create_board.get_piece([4, 4]).player == c.Players.WHITE
        for i in range(5):
            assert create_board.get_piece([2, i]) is None 

    def test_board_print_board(self, create_board):
        """
        Tests if the board is printed correctly.
        Check the output in the terminal.
        """
        print(create_board)

    
