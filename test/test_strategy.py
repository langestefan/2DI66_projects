import pytest
import numpy as np

import assignment_1.constants as c
from assignment_1.board import ChessBoard
from assignment_1.strategy import RandomStrategy


class TestStrategy:
    @pytest.fixture(autouse=True)
    def create_strategy(self):
        """
        Creates a chess board object
        """
        return RandomStrategy(player=c.Players.WHITE)

    @pytest.fixture(autouse=True)
    def create_board(self):
        """
        Creates a chess board object
        """
        return ChessBoard()

    def test_strategy_creation(self, create_strategy):
        """
        Tests if the strategy is created correctly.
        """
        assert create_strategy is not None
        assert create_strategy.player == c.Players.WHITE

    def test_strategy_get_move(self, create_strategy, create_board):
        """
        Tests if the correct move is retrieved.
        """
        assert create_strategy.get_move(create_board) is not None
        assert type(create_strategy.get_move(create_board)) is np.ndarray
        assert create_strategy.get_move(create_board).shape[1] == 4
