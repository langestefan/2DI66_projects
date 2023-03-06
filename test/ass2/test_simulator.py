import pytest
from scipy import stats

# to enable parent directory imports
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from assignment_2.simulation import QueueSimulator
from assignment_2.dist.Distribution import Distribution


class TestSimulator:
    @pytest.fixture(autouse=True)
    def create_simulator(self):
        """
        Creates a game state object.
        """
        distributions = [Distribution(stats.poisson(1))]
        distributions.append(Distribution(stats.expon(scale=1 / 80)))
        distributions.append(Distribution(stats.geom(1 / 3)))
        distributions.append(Distribution(stats.bernoulli(0.4)))
        distributions.append(Distribution(stats.expon(scale=1 / 20)))
        distributions.append(Distribution(stats.expon(scale=1 / 12)))

        return QueueSimulator(distributions, 1, 3, False, False, 1)

    @pytest.fixture(autouse=True)
    def test_simulator_init(self, create_simulator):
        """
        Tests the initialization of the simulator.
        """
        assert create_simulator.sim_history is not None
        assert create_simulator.parallelize is False

    def test_simulator_run(self, create_simulator):
        """
        Tests the run method of the simulator.
        """
        create_simulator.run(n=1)
        assert create_simulator.sim_history.get_number_of_simulations() == 1
