from conftest import Context as ctx
import assignment_1.constants as c

import pytest


from assignment_1.simulator import ChessSimulator


class TestSimulator:
    @pytest.fixture(autouse=True)
    def create_simulator(self):
        """
        Creates a game state object.
        """
        return ChessSimulator()

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
