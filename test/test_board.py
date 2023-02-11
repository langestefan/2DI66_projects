import pytest
import numpy as np
import copy

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
        assert create_board.get_board_arr() is not None
        assert create_board.get_board_arr().shape == (
            c.BOARD_SIZE,
            c.BOARD_SIZE,
        )

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

    def test_get_all_pieces(self, create_board):
        """
        Tests if the correct pieces are retrieved.
        """
        all_pieces_white = create_board.get_all_pieces(c.Players.WHITE)
        assert type(all_pieces_white) is list
        assert len(all_pieces_white) == c.n_pieces
        assert all_pieces_white[0].player == c.Players.WHITE

    def test_move_piece_board(self, create_board):
        """
        Tests if the piece is moved correctly.
        """
        old_pos = np.array([1, 0])
        new_pos = np.array([2, 0])
        assert create_board.get_piece(new_pos) is None
        create_board.move_piece(old_pos, new_pos, c.Players.BLACK)
        assert create_board.get_piece(old_pos) is None
        assert create_board.get_piece(new_pos) is not None

        # move same piece again
        old_pos = new_pos
        new_pos = np.array([3, 0])
        create_board.move_piece(old_pos, new_pos, c.Players.BLACK)
        assert create_board.get_piece(old_pos) is None
        assert create_board.get_piece(new_pos) is not None

    def test_board_copy(self, create_board):
        """
        Tests if the board is copied correctly.
        """
        board_copy: np.ndarray = copy.copy(create_board)
        assert board_copy is not None
        assert board_copy.shape == (c.BOARD_SIZE, c.BOARD_SIZE)
        assert board_copy[0, 0] is not None
        assert board_copy[0, 0].name == "King"
        assert board_copy[0, 0].player == c.Players.BLACK
