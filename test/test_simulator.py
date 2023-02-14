import pytest

from assignment_1.simulator import ChessSimulator
from assignment_1.board import ChessBoard


class TestSimulator:
    @pytest.fixture(autouse=True)
    def create_simulator(self):
        """
        Creates a game state object.
        """
        return ChessSimulator()

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
