from collections import deque
from scipy import stats
from abc import ABC, abstractmethod
import numpy as np
import random
import multiprocessing as mp
import logging

# from assignment_2.dist.Distribution import Distribution

# from assignment_2.customer import Customer
from assignment_2.group import Group
# from assignment_2.pqueue import Queue
# from assignment_2.server import Server
from assignment_2.event import Event
from assignment_2.simresults import SimResults
from assignment_2.fes import FES

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        "[%(asctime)s] %(levelname)s [%(name)s::%(className)s:%(lineno)s]"
        " %(message)s"
    ),
)

logger = logging.getLogger(__name__)

conf_to_z = {
    0.90: 1.645,
    0.95: 1.960,
    0.99: 2.576,
}


class SimHistory:
    def __init__(self):
        self.logstr = {"className": self.__class__.__name__}
        self.sim_runs: list[SimResults] = []
        self.nr_simulations = 0

    def __str__(self):
        str = f"Number of simulations: {self.nr_simulations}"

        return str

    def add_sim_run(self, sim_result):
        """
        Adds a game run to the game runs.

        :param game_run: The game run to be added.
        """
        self.sim_runs.append(sim_result)
        self.sim_runs += 1

    def get_sim_runs(self) -> list:
        """
        Returns the list containing all game runs.

        :return: The game runs.
        """
        return self.sim_runs

    def get_number_of_simulations(self) -> int:
        """
        Returns the number of games played.

        :return: The number of games played.
        """
        return self.nr_simulations

    def get_statistics_all(self) -> dict:
        # for all queues together
        statistics = {
            "QueueLengths_all": deque(),
            "QueueLength_mean": 0.0,
            "QueueLength_std": 0.0,
            "QueueLength_normal_ci_95": 0.0,
            "WaitingTimes_all": deque(),
            "WaitingTime_mean": 0.0,
            "WaitingTime_std": 0.0,
            "WaitingTime_normal_ci_95": 0.0,
            "CustomersCanteen_all": deque(),
            "CustomersCanteen_mean": 0.0,
            "CustomersCanteen_std": 0.0,
            "CustomersCanteen_ci_95": 0.0,
            "SojournTimeCustomer_all": deque(),
            "SojournTimeCustomer_mean": 0.0,
            "SojournTimeCustomer_std": 0.0,
            "SojournTimeCustomer_normal_ci_95": 0.0,
            "SojournTimeGroup_all": deque(),
            "SojournTimeGroup_mean": 0.0,
            "SojournTimeGroup_std": 0.0,
            "SojournTimeGroup_normal_ci_95": 0.0,
        }

        for i, simulation in enumerate(self.sim_runs):
            allQL = simulation.getMeanQueueLength()
            allWT = simulation.getMeanWaitingTime()

            statistics["QueueLengths_all"].append(np.mean(allQL))
            statistics["WaitingTimes_all"].append(np.mean(allWT))
            statistics["CustomersCanteen_all"].append(
                simulation.getMeanCustomersCanteen()
            )
            statistics["SojournTimeCustomer_all"].append(
                simulation.getMeanSojournCustomer()
            )
            statistics["SojournTimeGroup_all"].append(
                simulation.getMeanSojournGroup()
            )

        statistics["QueueLength_mean"] = np.round(
            np.mean(statistics["QueueLengths_all"]), 3
        )
        statistics["QueueLength_std"] = np.round(
            np.std(statistics["QueueLengths_all"]), 3
        )
        statistics["WaitingTime_mean"] = np.round(
            np.mean(statistics["WaitingTime_all"]), 3
        )
        statistics["WaitingTime_std"] = np.round(
            np.std(statistics["WaitingTime_all"]), 3
        )
        statistics["CustomersCanteen_mean"] = np.round(
            np.mean(statistics["CustomersCanteen_all"]), 3
        )
        statistics["CustomersCanteen_std"] = np.round(
            np.std(statistics["CustomersCanteen_all"]), 3
        )
        statistics["SojournTimeCustomer_mean"] = np.round(
            np.mean(statistics["SojournTimeCustomer_all"]), 3
        )
        statistics["SojournTimeCustomer_std"] = np.round(
            np.std(statistics["SojournTimeCustomer_all"]), 3
        )
        statistics["SojournTimeGroup_mean"] = np.round(
            np.mean(statistics["SojournTimeGroup_all"]), 3
        )
        statistics["SojournTimeGorup_std"] = np.round(
            np.std(statistics["SojournTimeGroup_all"]), 3
        )

        statistics["QueueLength_normal_ci_95"] = self.__ci_normal(
            self.nr_simulations,
            statistics["QueueLength_mean"],
            statistics["QueueLength_std"] ** 2,
            0.95,
        )

        statistics["WaitingTime_normal_ci_95"] = self.__ci_normal(
            self.nr_simulations,
            statistics["WaitingTime_mean"],
            statistics["WaitingTime_std"] ** 2,
            0.95,
        )

        statistics["CustomersCanteen_normal_ci_95"] = self.__ci_normal(
            self.nr_simulations,
            statistics["CustomersCanteen_mean"],
            statistics["CustomersCanteen_std"] ** 2,
            0.95,
        )

        statistics["SojournTimeCustomer_normal_ci_95"] = self.__ci_normal(
            self.nr_simulations,
            statistics["SojournTimeCustomer_mean"],
            statistics["SojournTimeCustomer_std"] ** 2,
            0.95,
        )

        statistics["SojournTimeGroup_normal_ci_95"] = self.__ci_normal(
            self.nr_simulations,
            statistics["SojournTimeGroup_mean"],
            statistics["SojournTimeGroup_std"] ** 2,
            0.95,
        )

        return statistics

    def get_statistics_separate(self, queue_nr) -> dict:
        # per queue
        statistics = {
            "QueueLengths_all": deque(),
            "QueueLength_mean": 0.0,
            "QueueLength_std": 0.0,
            "QueueLength_normal_ci_95": 0.0,
            "WaitingTimes_all": deque(),
            "WaitingTime_mean": 0.0,
            "WaitingTime_std": 0.0,
            "WaitingTime_normal_ci_95": 0.0,
        }

        q = queue_nr

        for i, simulation in enumerate(self.sim_runs):
            statistics["QueueLengths_all"].append(
                simulation.getMeanQueueLength()[q]
            )
            statistics["WaitingTimes_all"].append(
                simulation.getMeanWaitingTime()[q]
            )

        statistics["QueueLength_mean"] = np.round(
            np.mean(statistics["QueueLengths_all"]), 3
        )
        statistics["QueueLength_std"] = np.round(
            np.std(statistics["QueueLengths_all"]), 3
        )
        statistics["WaitingTime_mean"] = np.round(
            np.mean(statistics["WaitingTime_all"]), 3
        )
        statistics["WaitingTime_std"] = np.round(
            np.std(statistics["WaitingTime_all"]), 3
        )

        statistics["QueueLength_normal_ci_95"] = self.__ci_normal(
            self.nr_simulations,
            statistics["QueueLength_mean"],
            statistics["QueueLength_std"] ** 2,
            0.95,
        )

        statistics["WaitingTime_normal_ci_95"] = self.__ci_normal(
            self.nr_simulations,
            statistics["WaitingTime_mean"],
            statistics["WaitingTime_std"] ** 2,
            0.95,
        )

        return statistics

    def __ci_normal(
        self, n: int, u: np.float32, var: np.float32, alpha: float
    ) -> tuple:
        """
        Computes the confidence interval for a normal distribution.

        :param n: The number of trials.
        :param u: The mean.
        :param var: The variance.
        :param alpha: The significance level.
        :return: The confidence interval.
        """

        # assume a normal distr. and get the confidence interval for the mean
        z = conf_to_z[alpha]
        u_up = np.round(u + z * np.sqrt(var / n), 3)
        u_low = np.round(u - z * np.sqrt(var / n), 3)

        # return the confidence interval
        return (u_low, u_up)


class Simulator(ABC):
    """
    A base class to represent a simulator.
    """

    def __init__(self, parallelize: bool, n_jobs: int):
        super().__init__()
        self.logstr = {"className": self.__class__.__name__}
        self.sim_history: SimHistory = SimHistory()
        self.parallelize = parallelize
        self.n_jobs: int = n_jobs

    def get_sim_history(self) -> SimHistory:
        """
        Returns the simulation history.

        :return: The simulation history.
        """
        if self.sim_history is None:
            raise ValueError(
                "Simulation history is not initialized. Did you call run()?"
            )
        return self.sim_history

    def run(self, n: int) -> None:
        """
        Starts the simulation.

        :param n: The number of simulation runs to perform.
        """
        # the results of the simulation runs will be written to the game history
        self.__do_n_runs(n, self.sim_history, self.parallelize)

    def __do_n_runs(
        self,
        n: int,
        sim_history: SimHistory,
        parallelize: bool = False,
    ) -> None:
        """
        Runs n simulations.

        :param n: The number of simulation runs to perform.
        :param parallelize: Whether to parallelize the simulation.
        """
        # if parallelization is enabled, use multiprocessing
        if parallelize:
            with mp.Pool(processes=self.n_jobs) as pool:
                results = pool.map(self._do_one_run, range(n))

                # add the results to the game history
                for result in results:
                    sim_history.add_sim_run(result)
        else:
            for i in range(n):
                result = self._do_one_run(i)
                sim_history.add_sim_run(result)

    @abstractmethod
    def _do_one_run(self, T: int) -> SimResults:
        """
        Runs one game.

        :param n: The number of the game run.
        """
        pass


class QueueSimulator(Simulator):
    def __init__(
        self,
        distributions,
        nr_servers: int = 1,
        nr_queues: int = 3,
        print_status: bool = True,
        parallelize: bool = False,
        n_jobs: int = 1,
    ):
        self.nr_queues = nr_queues
        self.arrDist = distributions[0]
        self.grabDist = distributions[1]
        self.groupDist = distributions[2]
        # includes distribution for choice between payment methods
        # and distribution for serving time per payment method
        # for each Queue (so ind = 2,3 = queue 1, ind = 4,5 = queue 2 etc.)
        # note that if only one payment method is possible, len(self.servDist) = 1
        self.servDist = distributions[3:]

        self.nr_servers = nr_servers
        self.queues = np.zeros((nr_queues, 1))
        self.print = print_status

        super().__init__(parallelize=parallelize, n_jobs=n_jobs)

    def _do_one_run(self, T: int) -> SimResults:
        fes = FES()  # future event set
        self.res = SimResults(len(self.queues))  # simulation results
        t = 0  # current time

        # TODO: Implement class Queue and it accepting distributions
        # TODO: class Queue also creates Server objects
        # initialize queues
        for q in range(self.nr_queues):
            self.queues[q] = Queue(self.servDist, self.nr_servers)

        # initial customers
        g, c = self.create_new_group(t, T)  # first group
        N = len(c)

        while t < T or N > 0:  # main loop
            self.res.registerCanteen(N)
            lengths = self.get_queue_lengths()  # current queue lengths
            self.res.registerQueueLength(t, lengths)  # register queue lengths

            # get next event
            e = fes.next()  # jump to next event
            t = e.time  # update the time
            c1 = e.customer  # customer associated with this event

            if e.type == Event.ARRIVAL:  # handle an arrival event
                shortest = np.where(lengths == np.amin(t))[
                    0
                ]  # get index of shortest queue
                q = random.choice(
                    shortest
                )  # get (random if same length) shortest queue

                # TODO: Implement class Customer adding queue number
                c1.add_queue(q)  # add queue number to customer object

                # TODO: Implement class Queue adding customers
                self.queues[q].add_customer(c1)  # add customer to queue

                # TODO: Implement class Queue.get_length()
                # TODO: Implement Queue.sample_servDist()
                if (
                    self.queues[q].get_length() <= self.queues[q].nr_servers
                ):  # there was a free server
                    self.res.registerWaitingTime(t - c1.arrivalTime)
                    servT = self.queues[q].sample_servDist()
                    dep = Event(Event.DEPARTURE, t + servT, c1)
                    fes.add(dep)  # schedule his departure

                    # TODO: implement Customer.register_depTime
                    c1.register_depTime(t + servT)
                    self.res.registerSojournTime(c1)

                g, c2 = self.create_new_group(t, T)  # create next arrival
                N += len(c2)

            elif e.type == Event.DEPARTURE:  # handle a departure event
                # TODO: implement Queue.remove_customer()
                c1.get_queue().remove_customer(c)
                N -= 1

                # TODO: switch queues if one is shorter (EXTENSION)

                # TODO: implement Customer.get_queue() function
                if (
                    c1.get_queue().get_length() >= self.nr_servers
                ):  # someone was waiting
                    c2 = (
                        c1.get_queue().next_customer()
                    )  # longest waiting customer
                    self.res.registerWaitingTime(t - c2.arrivalTime)
                    servT = c1.get_queue().sample_servDist()
                    dep = Event(Event.DEPARTURE, t + servT, c2)
                    fes.add(dep)  # schedule this departure

                    c2.register_depTime(t + servT)
                    self.res.registerSojournTime(c2)

        return self.res

    def get_queue_lengths(self):
        length = np.array([len(x.length) for x in self.queues])

        if self.print:
            print(f"Current queue lengths: {length}")

        return length

    def create_new_group(self, t, T):
        # TODO: Implement class Group also creating Customer objects & returning array with customers
        # TODO: Implement class Customer initializing arrivalTime = arrDist.rvs() + grabDist.rvs()
        # TODO: Implement class Customer adding ARRIVAL event to FES
        # TODO: Give addCustomers method variable t to check if arrivalTime at canteen
        # so excluding grabbing food time, is below T

        g = Group(self.groupDist.rvs(), self.grabDist, self.arrDist)
        c = g.addCustomers(t, T)  # also adds arrival time to queue to fes
        self.res.registerGroup(g, c)

        if self.print:
            print(f"Created new group consisting of {g.nrCustomers} customers")

        return g, c


# =============================================================================
# arrDist = Distribution(stats.expon(scale=1/2.4)) # interarrival time distr.
# servDist = Distribution(stats.expon(scale=1/1.0)) # service time distribution
# sim = Simulation(arrDist, servDist, 3) # the simulation model
# res = sim.simulate(100000)  # perform simulation
# print(res)  # print the results
# res.histQueueLength()  # plot of the queue length
# res.histWaitingTimes()  # histogram of waiting times
# =============================================================================
