from collections import deque
from abc import ABC, abstractmethod
import numpy as np
import multiprocessing as mp
import logging
import time

import random
import scipy.stats as stats
from dist.distribution import Distribution

import assignment_2.constants as c

from assignment_2.event import Event
from assignment_2.simresults import SimResults
from assignment_2.fes import FES
from assignment_2.group import Group
from assignment_2.customer import Customer
from assignment_2.cqueue import CQueue
from assignment_2.server import Server


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
        self.nr_simulations += 1

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

    def __init__(self, n_jobs: int):
        super().__init__()
        self.logstr = {"className": self.__class__.__name__}
        self.sim_history: SimHistory = SimHistory()
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
        self.__do_n_runs(n)

    def __do_n_runs(self, n: int) -> None:
        """
        Runs n simulations.

        :param n: The number of simulation runs to perform
        """
        # if parallelization is enabled, use multiprocessing
        if self.n_jobs > 1:
            with mp.Pool(processes=self.n_jobs) as pool:
                results = pool.map(self._do_one_run, range(n))

                # add the results to the sim history
                for result in results:
                    self.sim_history.add_sim_run(result)
        else:
            for i in range(n):
                result = self._do_one_run(i)
                self.sim_history.add_sim_run(result)

    @abstractmethod
    def _do_one_run(self, n: int) -> SimResults:
        """
        Runs one game.

        :param n: The number of the game run.
        """
        pass


class QueueSimulator(Simulator):
    def __init__(
        self,
        nr_servers: int = 3,
        nr_queues: int = 3,
        n_jobs: int = 1,
    ):
        self.logstr = {"className": self.__class__.__name__}
        self.nr_queues = nr_queues
        self.nr_servers = nr_servers

        logger.debug(f'Nr. of queues: {nr_queues}, nr. of servers: {nr_servers}', extra=self.logstr)

        # we currently only support one server per queue
        if nr_servers != nr_queues:
            raise ValueError(
                "Number of servers must be equal to number of queues."
            )

        self.queues = np.empty(nr_queues, dtype=CQueue)
        self.servers = np.empty(nr_servers, dtype=Server)

        # simulation history
        self.sim_history: SimHistory = SimHistory()

        # geometric distribution for the group size N
        self.group_size_dist = Distribution(stats.geom(c.P_GROUP_SIZE))

        # exponential distribution for the arrival time of a group
        self.arrival_time_dist = [
            Distribution(stats.expon(scale=mu)) for mu in c.MU_ARRIVAL_RATE_SEC
        ]

        # exponential distribution for the time it takes a customer to grab food
        self.grab_food_dist = Distribution(
            stats.expon(scale=c.MU_CUSTOM_GRAB_FOOD)
        )

        # bernoulli distribution for cash or card payment with p = p_cash
        self.use_cash_dist = Distribution(stats.bernoulli(c.P_CASH))

        super().__init__(n_jobs=n_jobs)

    def _do_one_run(self, n: int) -> None:
        """
        Runs a simulation with every rate parameter specified.

        :param n: The number of the simulation run.
        :return: The simulation results.
        """
        # run simulation once for each rate parameter
        for idx, dist in enumerate(self.arrival_time_dist):
            logger.debug(
                (
                    f"Running new simulation {n} with rate parameter:"
                    f" {c.MU_ARRIVAL_RATE_MIN[idx]} / min"
                ),
                extra=self.logstr,
            )
            # initialize queues
            for q_id in range(self.nr_queues):
                self.queues[q_id] = CQueue(queue_id=q_id)

            # initialize servers
            for s in range(self.nr_servers):
                self.servers[s] = Server(
                    id=s, mu_cash=c.MU_SERVICE_CASH, mu_card=c.MU_SERVICE_BANK
                )

            # add servers to each queue
            assert (self.nr_servers % self.nr_queues == 0), "Number of servers must be divisible by number of queues."
            nr_servers_per_queue = self.nr_servers // self.nr_queues
            logger.debug(
                f"Number of servers per queue: {nr_servers_per_queue}",
                extra=self.logstr,
            )

            for queue in self.queues:
                for s in range(nr_servers_per_queue):
                    queue.add_server(self.servers[s])

            # run simulation
            self.simulate_queue()

    def simulate_queue(self) -> None:
        """
        Runs one full simulation.

        :return: The simulation results.
        """
        # debug variables to keep track of stuff
        n_arrivals = 0
        n_departures = 0

        # initialize simulation
        fes = FES()
        self.res = SimResults(self.queues.size)
        t = 0

        # create first group and update the FES with new arrival events
        fes = self.create_new_group(t_arr=t, fes=fes)

        # run simulation until t > SIM_T
        while t < c.SIM_T:
            time.sleep(0.5)
            logger.debug(f'FES: \n{fes}', extra=self.logstr)
            # TODO: register canteen occupancy (number of customers in canteen)
            # TODO: register queue lengths
            # TODO: register waiting times

            # get queue lengths
            q_lengths = self.get_queue_lengths()

            # get next event from FES
            e = fes.next()  # jump to next event
            t = e.time  # update time
            cust = e.get_customer()  # get customer

            logger.debug(f"Event: {e}", extra=self.logstr)

            # handle customer arrival event
            if e.type == Event.ARRIVAL:
                n_arrivals += 1
                logger.debug(f'--- ARRIVAL total: {n_arrivals} ---', extra=self.logstr)

                # get the queue with the shortest length
                shortest = np.where(q_lengths == np.amin(q_lengths))[0]
                q_id = random.choice(shortest)
                logger.debug(
                    f"Shortest queue: {shortest}, selected queue: {q_id}",
                    extra=self.logstr,
                )

                # add customer to queue object
                self.queues[q_id].add_customer(customer=cust, q_id=q_id)  # type: ignore

                # store q_id in customer object
                cust.set_queue_id(q_id)

                # if there was a free server we schedule a departure event
                if self.queues[q_id].get_length() <= self.queues[q_id].get_n_servers():  # type: ignore
                    # get the server that will serve the customer
                    # TODO: for now we only support one server per queue so id is always 0
                    server = self.queues[q_id].get_server(server_id=0)  # type: ignore
                    t_service = t + server.get_service_time(
                        cust.get_uses_cash()
                    )

                    # schedule departure event
                    dep_event = Event(Event.DEPARTURE, t_service, cust)
                    fes.add(dep_event)

                # create new group and update the FES with new arrival events
                fes = self.create_new_group(t_arr=t, fes=fes)

            # handle customer departure event
            elif e.type == Event.DEPARTURE:
                n_departures += 1
                logger.debug(f'--- DEPARTURE total: {n_departures} ---', extra=self.logstr)
                # get the queue the customer is in and remove the customer from that queue
                # TODO: do we check each queue if the customer is there or do we just store the queue id in the customer obj?
                q_id = cust.get_queue_id()
                self.queues[q_id].remove_customer(customer=cust, q_id=q_id)  # type: ignore

                # if there are customers waiting we schedule a departure event for the next customer
                nr_servers = self.queues[q_id].get_n_servers()  # type: ignore
                if self.queues[q_id].get_length() >= nr_servers:  # type: ignore

                    # get the next customer in the queue
                    cust = self.queues[q_id].get_customer_at_pos(pos=nr_servers - 1)  # type: ignore

                    # get the server that will serve the customer
                    server = self.queues[q_id].get_server(server_id=0)  # type: ignore
                    t_service = t + server.get_service_time(
                        cust.get_uses_cash()
                    )

                    # schedule departure event
                    dep_event = Event(Event.DEPARTURE, t_service, cust)
                    fes.add(dep_event)

    def create_new_group(self, t_arr: float, fes: FES) -> FES:
        """
        Create a new group of customers.

        :param t_arr: The arrival time of the group.
        :param fes: The current future event schedule before the group arrived.
        :return: The updated future event schedule after the group arrived.
        """
        # sample distributions for group size, arrival time and grab time and cash usage
        n_customers = self.group_size_dist.rvs(1)
        t_grab = t_arr + self.grab_food_dist.rvs(n_customers)
        use_cash = self.use_cash_dist.rvs(n_customers)

        # create group of customers
        group = Group(n_customers, use_cash, t_arr, t_grab)

        # create an arrival event for each customer in the group, and add it to the FES
        for idx, customer in enumerate(group.get_customers()):
            fes.add(Event(Event.ARRIVAL, customer.get_t_done_grab(), customer))

        return fes

    def get_queue_lengths(self) -> np.ndarray:
        """
        Get the length of each queue.

        Also set the shortest queue.

        :return: The current queue lengths stored in a numpy array.
        """
        lengths = np.array([q_id.get_length() for q_id in self.queues])
        logger.debug(f"Current queue lengths: {lengths}", extra=self.logstr)

        return lengths
