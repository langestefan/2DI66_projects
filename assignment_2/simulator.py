from abc import ABC, abstractmethod
import multiprocessing as mp
import logging
from scipy import stats

from dist.Distribution import Distribution

logger = logging.getLogger(__name__)

conf_to_z = {
    0.90: 1.645,
    0.95: 1.960,
    0.99: 2.576,
}


class Simulator(ABC):
    """
    A base class to represent a simulator.
    """

    def __init__(self, n_jobs: int):
        super().__init__()
        self.logstr = {"className": self.__class__.__name__}
        self.n_jobs: int = n_jobs

    def run(self, n: int) -> None:
        """
        Starts the simulation.

        :param n: The number of simulation runs to perform.
        """
        # the results of the simulation runs will be written to the game history
        self.__do_n_runs(n)

    def __do_n_runs(self, n: int) -> None:
        """
        Runs n simulations.

        :param n: The number of simulation runs to perform.
        :param parallelize: Whether to parallelize the simulation.
        """

        # if parallelization is enabled, use multiprocessing
        if self.n_jobs > 1:
            with mp.Pool(processes=self.n_jobs) as pool:
                results = pool.map(self._do_one_run, range(n))

                # add the results to the game history
                for result in results:
                    pass
        else:
            for i in range(n):
                # result = self._do_one_run(i)
                pass

    @abstractmethod
    def _do_one_run(self) -> None:
        """
        Runs one game.

        :param n: The number of the game run.
        """
        pass


class QueueSimulator(Simulator):
    """
    Queue specific simulation details.
    """

    def __init__(self, n_jobs: int):
        super().__init__(n_jobs)

    def _do_one_run(self) -> None:

        # make a distribution only for testing
        mu = 3.4
        sigma = 1.5
        normDist = stats.norm(mu, sigma)
        myDist = Distribution(normDist)

        return None
