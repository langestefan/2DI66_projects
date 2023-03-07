import pytest
from scipy import stats

# to enable parent directory imports
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from assignment_2.simulator import QueueSimulator


class TestSimulator:
    @pytest.fixture(autouse=True)
    def create_simulator(self):
        """
        Creates a game state object.
        """
        return QueueSimulator(nr_servers=1, nr_queues=1, n_jobs=1)

    @pytest.fixture(autouse=True)
    def test_simulator_init(self, create_simulator):
        """
        Tests the initialization of the simulator.
        """
        assert create_simulator.sim_history is not None

    def test_simulator_run(self, create_simulator):
        """
        Tests the run method of the simulator.
        """
        create_simulator.run(n=1)
        assert create_simulator.sim_history.get_number_of_simulations() == 1
