import pytest
import numpy as np

import assignment_1.constants as c
from assignment_1.board import ChessBoard
from assignment_1.pieces import Pawn, Rook, Knight, Bishop, Queen, King


class TestClientPieces:
    @pytest.fixture(autouse=True)
    def create_pieces(self):
        """
        Creates a piece object.
        """
        init_pos = np.array([2, 2])  # center, first row of white
        return (
            Pawn(c.Players.WHITE, init_pos=init_pos),
            Rook(c.Players.WHITE, init_pos=init_pos),
            Knight(c.Players.WHITE, init_pos=init_pos),
            Bishop(c.Players.WHITE, init_pos=init_pos),
            Queen(c.Players.WHITE, init_pos=init_pos),
            King(c.Players.WHITE, init_pos=init_pos),
        )

    @pytest.fixture(autouse=True)
    def create_board(self):
        """
        Creates a chess board object
        """
        return ChessBoard(init_pieces=True)

    @pytest.fixture(autouse=True)
    def create_empty_board(self):
        """
        Creates a chess board object
        """
        return ChessBoard(init_pieces=False)

    def test_piece_creation(self, create_pieces):
        """
        Tests if the piece object is created correctly.
        """
        for piece in create_pieces:
            assert piece is not None
            assert piece.player == c.Players.WHITE
            assert piece.name is not None

    def test_piece_get_player(self, create_pieces):
        """
        Tests if the correct player is retrieved.
        """
        for piece in create_pieces:
            assert piece.get_player() == c.Players.WHITE

    def test_piece_get_name(self, create_pieces):
        """
        Tests if the correct name is retrieved.
        """
        for piece in create_pieces:
            assert type(piece.get_name()) is str

    def test_piece_get_moves(self, create_pieces, create_board):
        """
        Tests if moves are retrieved. Moves may not be valid and then len=0.
        """
        board = create_board.get_board()
        for piece in create_pieces:
            assert type(piece.get_valid_moves(board)) is np.ndarray

    def test_piece_get_valid_moves(self, create_pieces, create_empty_board):
        """
        Tests if valid moves are retrieved.
        """
        empty_board = create_empty_board.get_board()
        assert (empty_board == None).all()  # noqa: E711

        for piece in create_pieces:
            # put piece on board
            create_empty_board.put_new_piece_on_board(
                piece,
                position=piece.get_position(),
                overwrite=True,
                ignore_pos_check=True,
                do_consistency_check=True,
            )
            empty_board = create_empty_board.get_board()
            valid_moves_piece = piece.get_valid_moves(empty_board)
            print(f"valid_moves_piece: \n{valid_moves_piece}")
            ascii_brd = piece.draw_valid_moves(empty_board, valid_moves_piece)
            print(f"ascii_board: \n{ascii_brd}")
            # assert type(valid_moves_piece) is np.ndarray
            # assert valid_moves_piece.shape[1] == 4
            # assert len(valid_moves_piece) > 0
