import pytest

# to enable parent directory imports
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from assignment_1.simulator import ChessSimulator
from assignment_1.board import ChessBoard
from assignment_1.strategy import RandomStrategy

import assignment_1.constants as c


class TestSimulator:
    @pytest.fixture(autouse=True)
    def create_simulator(self):
        """
        Creates a game state object.
        """
        return ChessSimulator(
            black_strat=RandomStrategy(player=c.Players.BLACK),
            white_strat=RandomStrategy(player=c.Players.WHITE),
        )

    @pytest.fixture(autouse=True)
    def create_empty_board(self):
        """
        Creates a chess board object
        """
        return ChessBoard(init_pieces=False)

    def test_simulator_init(self, create_simulator):
        """
        Tests the initialization of the simulator.
        """
        assert create_simulator.game_history is not None
        assert create_simulator.parallelize is False

    def test_simulator_run(self, create_simulator):
        """
        Tests the run method of the simulator.
        """
        create_simulator.run(n=1)
        assert create_simulator.game_history.get_number_of_games_played() == 1
