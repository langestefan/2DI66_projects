import pytest

import assignment_1.constants as c
from assignment_1.board import ChessBoard
from assignment_1.strategy import RandomStrategy
from assignment_1.game_state import GameState


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

    def create_game_state(self):
        """
        Creates a game state object.
        """
        return GameState()

    def test_strategy_creation(self, create_strategy):
        """
        Tests if the strategy is created correctly.
        """
        assert create_strategy is not None
        assert create_strategy.player == c.Players.WHITE

    # def test_strategy_get_move(self, create_game_state, create_strategy):
    #     """
    #     Tests if the correct move is retrieved.
    #     """
    #     pass
