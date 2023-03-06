import pytest
import numpy as np

# to enable parent directory imports
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import assignment_1.constants as c
from assignment_1.board import ChessBoard
from assignment_1.pieces import Pawn, Rook, Knight, Bishop, Queen, King


class TestClientPieces:
    @pytest.fixture(autouse=True)
    def create_pieces_white(self):
        """
        Creates a piece object.
        """
        init_pos = np.array([2, 2])  # center, first row of white
        return (
            Pawn(c.Players.WHITE, init_pos=init_pos, extra_step=True),
            Rook(c.Players.WHITE, init_pos=init_pos),
            Knight(c.Players.WHITE, init_pos=init_pos),
            Bishop(c.Players.WHITE, init_pos=init_pos),
            Queen(c.Players.WHITE, init_pos=init_pos),
            King(c.Players.WHITE, init_pos=init_pos),
        )

    @pytest.fixture(autouse=True)
    def create_pieces_black(self):
        """
        Creates a piece object.
        """
        init_pos = np.array([2, 2])  # center, first row of white
        return (
            Pawn(c.Players.BLACK, init_pos=init_pos, extra_step=True),
            Rook(c.Players.BLACK, init_pos=init_pos),
            Knight(c.Players.BLACK, init_pos=init_pos),
            Bishop(c.Players.BLACK, init_pos=init_pos),
            Queen(c.Players.BLACK, init_pos=init_pos),
            King(c.Players.BLACK, init_pos=init_pos),
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

    def test_piece_creation(self, create_pieces_white):
        """
        Tests if the piece object is created correctly.
        """
        for piece in create_pieces_white:
            assert piece is not None
            assert piece.player == c.Players.WHITE
            assert piece.name is not None

    def test_piece_get_player(self, create_pieces_white):
        """
        Tests if the correct player is retrieved.
        """
        for piece in create_pieces_white:
            assert piece.get_player() == c.Players.WHITE

    def test_piece_get_name(self, create_pieces_white):
        """
        Tests if the correct name is retrieved.
        """
        for piece in create_pieces_white:
            assert type(piece.get_name()) is str

    def test_piece_get_moves(self, create_pieces_white, create_board):
        """
        Tests if moves are retrieved. Moves may not be valid and then len=0.
        """
        board = create_board.get_board_arr()
        for piece in create_pieces_white:
            assert type(piece.get_piece_moves(board)) is np.ndarray

    def test_piece_get_valid_moves_white(
        self, create_pieces_white, create_empty_board
    ):
        """
        Tests if valid moves are retrieved.
        """
        empty_board = create_empty_board.get_board_arr()
        assert (empty_board == None).all()  # noqa: E711

        for piece in create_pieces_white:
            # put piece on board
            create_empty_board.put_new_piece_on_board(
                piece,
                position=piece.get_position(),
                overwrite=True,
                ignore_pos_check=True,
                do_consistency_check=True,
            )
            empty_board = create_empty_board.get_board_arr()
            valid_moves_piece = piece.get_piece_moves(empty_board)
            # print(f"valid_moves_piece: \n{valid_moves_piece}")
            ascii_brd = piece.draw_valid_moves(empty_board, valid_moves_piece)
            print(f"ascii_board: \n{ascii_brd}")

    def test_piece_get_valid_moves_black(
        self, create_pieces_black, create_empty_board
    ):
        """
        Tests if valid moves are retrieved.
        """
        empty_board = create_empty_board.get_board_arr()
        assert (empty_board == None).all()  # noqa: E711

        for piece in create_pieces_black:
            # put piece on board
            create_empty_board.put_new_piece_on_board(
                piece,
                position=piece.get_position(),
                overwrite=True,
                ignore_pos_check=True,
                do_consistency_check=True,
            )
            empty_board = create_empty_board.get_board_arr()
            valid_moves_piece = piece.get_piece_moves(empty_board)
            # print(f"valid_moves_piece: \n{valid_moves_piece}")
            ascii_brd = piece.draw_valid_moves(empty_board, valid_moves_piece)
            print(f"ascii_board: \n{ascii_brd}")

    def test_pawn_moves(self, create_empty_board):
        """
        Tests if valid moves are retrieved.
        """
        init_pos = np.array([2, 2])  # center

        # create pawns
        pawn_white_es = Pawn(
            c.Players.WHITE, init_pos=init_pos, extra_step=True
        )
        pawn_white = Pawn(c.Players.WHITE, init_pos=init_pos, extra_step=False)
        pawn_black_es = Pawn(
            c.Players.BLACK, init_pos=init_pos, extra_step=True
        )
        pawn_black = Pawn(c.Players.BLACK, init_pos=init_pos, extra_step=False)

        # test white pawn with extra step
        create_empty_board.put_new_piece_on_board(
            pawn_white_es,
            position=pawn_white_es.get_position(),
            overwrite=True,
            ignore_pos_check=True,
            do_consistency_check=True,
        )
        empty_board = create_empty_board.get_board_arr()
        valid_moves_piece = pawn_white_es.get_piece_moves(empty_board)
        assert (
            valid_moves_piece == np.array([[2, 2, 1, 2], [2, 2, 0, 2]])
        ).all()

        # test white pawn without extra step
        create_empty_board.put_new_piece_on_board(
            pawn_white,
            position=pawn_white.get_position(),
            overwrite=True,
            ignore_pos_check=True,
            do_consistency_check=True,
        )
        empty_board = create_empty_board.get_board_arr()
        valid_moves_piece = pawn_white.get_piece_moves(empty_board)
        print(f"valid_moves_piece: \n{valid_moves_piece}")
        assert (valid_moves_piece == np.array([[2, 2, 1, 2]])).all()

        # test black pawn with extra step
        create_empty_board.put_new_piece_on_board(
            pawn_black_es,
            position=pawn_black_es.get_position(),
            overwrite=True,
            ignore_pos_check=True,
            do_consistency_check=True,
        )
        empty_board = create_empty_board.get_board_arr()
        valid_moves_piece = pawn_black_es.get_piece_moves(empty_board)
        assert (
            valid_moves_piece == np.array([[2, 2, 3, 2], [2, 2, 4, 2]])
        ).all()

        # test black pawn without extra step
        create_empty_board.put_new_piece_on_board(
            pawn_black,
            position=pawn_black.get_position(),
            overwrite=True,
            ignore_pos_check=True,
            do_consistency_check=True,
        )
        empty_board = create_empty_board.get_board_arr()
        valid_moves_piece = pawn_black.get_piece_moves(empty_board)
        assert (valid_moves_piece == np.array([[2, 2, 3, 2]])).all()
