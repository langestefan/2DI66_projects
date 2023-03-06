import pytest
import numpy as np
import os

# to enable parent directory imports
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import assignment_1.constants as c
from assignment_1.game_state import GameState
from assignment_1.board import ChessBoard
from assignment_1.pieces import Rook, King


class TestClientGameState:
    @pytest.fixture(autouse=True)
    def create_game_state(self):
        """
        Creates a game state object.
        """
        return GameState()

    @pytest.fixture(autouse=True)
    def create_empty_board(self):
        """
        Creates a chess board object
        """
        return ChessBoard(init_pieces=False)

    def test_game_state_creation(self, create_game_state):
        """
        Tests if the game state object is created correctly.
        """
        assert create_game_state is not None
        assert create_game_state.get_round_number() == -1
        create_game_state.start_new_round(move=np.array([4, 4, 2, 2]))
        assert create_game_state.get_current_player() == c.Players.WHITE

    def test_game_state_start_new_round(self, create_game_state):
        """
        Tests if the round number is incremented correctly.
        """
        create_game_state.increment_round_number()
        create_game_state.start_new_round(move=np.array([4, 4, 2, 2]))
        assert create_game_state.get_current_player() == c.Players.WHITE
        create_game_state.increment_round_number()
        create_game_state.start_new_round(move=np.array([0, 0, 2, 3]))
        assert create_game_state.get_round_number() == 1
        assert create_game_state.get_current_player() == c.Players.BLACK

    def test_game_state_king_check_rook(
        self, create_empty_board, create_game_state
    ):
        """
        Tests if the king is in check.
        """
        # put king on the board
        king_pos = np.array([4, 2])
        king_piece = King(c.Players.WHITE, init_pos=king_pos)
        create_empty_board.put_new_piece_on_board(
            king_piece,
            position=king_pos,
            overwrite=True,
            ignore_pos_check=True,
            do_consistency_check=True,
        )

        # put rook on the board
        rook_pos = np.array([2, 2])
        rook_piece = Rook(c.Players.BLACK, init_pos=rook_pos)
        create_empty_board.put_new_piece_on_board(
            rook_piece,
            position=rook_pos,
            overwrite=True,
            ignore_pos_check=True,
            do_consistency_check=True,
        )

        # write the board to the game state
        create_game_state.chess_board = create_empty_board

        # print the board
        print(create_game_state.chess_board)

        create_game_state.increment_round_number()
        print(f"Current player: {create_game_state.get_current_player()}")
        print(f"Current round: {create_game_state.get_round_number()}")
        king_in_check = create_game_state.king_is_in_check(
            player=c.Players.WHITE
        )
        assert king_in_check is True
