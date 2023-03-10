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
    level=c.LOG_LEVEL,
    format=(
        "[%(asctime)s] %(levelname)s [%(name)s::%(className)s:%(lineno)s]"
        " %(message)s"
    ),
)

logger = logging.getLogger(__name__)
logging.getLogger('numexpr').setLevel(logging.WARNING)

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
        Adds a simulation run to the sim runs.

        :param sim_results: The simulation run to be added.
        """
        self.sim_runs.append(sim_result)
        self.nr_simulations += 1

    def get_sim_runs(self) -> list:
        """
        Returns the list containing all simulation runs.

        :return: The simulation runs.
        """
        return self.sim_runs

    def get_number_of_simulations(self) -> int:
        """
        Returns the number of simulations.

        :return: The number of simulations.
        """
        return self.nr_simulations

    def get_statistics_all(self, lam) -> dict:
        """
        Gathers statistics of results for all queues together
        
        :param lam: Index of rate parameter value for which statistics needs
            to be calculated 
            
        :return: Dictionary with statistics
        """
        statistics = {
            "QueueLengths_all": deque(), # list of all means 
            "QueueLength_mean": 0.0,
            "QueueLength_std": 0.0,
            "QueueLength_normal_ci_95": 0.0,
            "QueueLength_hist": np.zeros(SimResults.MAX_ENTRIES+1), # hist plot data
            "WaitingTime_all": deque(), # list of all  means 
            "WaitingTime_mean": 0.0,
            "WaitingTime_std": 0.0,
            "WaitingTime_normal_ci_95": 0.0,
            "CustomersCanteen_all": deque(), # list of all means 
            "CustomersCanteen_values": deque(), # list of all values (not averages)
            "CustomersCanteen_times": deque(), # list of time corresponding with _values
            "CustomersCanteen_mean": 0.0,
            "CustomersCanteen_std": 0.0,
            "CustomersCanteen_normal_ci_95": 0.0,
            "SojournTimeCustomer_all": deque(), # list of all means
            "SojournTimeCustomer_mean": 0.0,
            "SojournTimeCustomer_std": 0.0,
            "SojournTimeCustomer_normal_ci_95": 0.0,
            "SojournTimeGroup_all": deque(), # list of all means 
            "SojournTimeGroup_mean": 0.0,
            "SojournTimeGroup_std": 0.0,
            "SojournTimeGroup_normal_ci_95": 0.0
        }
        
        # go over all simulation runs 
        for i, simulation in enumerate(self.sim_runs):
            simulation = simulation[lam] # get simulation with correct rate parameter
            
            # update statistics
            allQL = simulation.get_mean_ql()
            allWT = simulation.get_mean_wait_t()
            
            statistics["QueueLengths_all"].append(np.mean(allQL))
            for q in range(simulation.nrQueues):
                statistics["QueueLength_hist"] += simulation.get_ql_hist(q)
            
            statistics["WaitingTime_all"].append(np.mean(allWT))
            
            statistics["CustomersCanteen_all"].append(
                simulation.get_mean_cust_canteen()
            )
            statistics["CustomersCanteen_values"] += simulation.canteen
            statistics["CustomersCanteen_times"] += simulation.canteen_times
            
            
            statistics["SojournTimeCustomer_all"].append(
                simulation.get_mean_sojourn_cust()
            )
            statistics["SojournTimeGroup_all"].append(
                simulation.get_mean_sojourn_group()
            )
        
        statistics["QueueLength_hist"] = statistics["QueueLength_hist"]/(i+1)
            
        # calculate mean and std 
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
        statistics["SojournTimeGroup_std"] = np.round(
            np.std(statistics["SojournTimeGroup_all"]), 3
        )

        # calculate 95% confidence intervals
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

    def get_statistics_separate(self, lam, queue_nr) -> dict:
        """
        Gathers statistics of results for queues separately
        
        :param lam: Index of rate parameter value for which statistics needs
            to be calculated 
        :param queue_nr: Integer indicating for which queue statistics need to 
            be calculated (same as queue_id)
            
        :return: Dictionary with statistics
        """
        statistics = {
            "QueueLengths_all": deque(),
            "QueueLength_mean": 0.0,
            "QueueLength_std": 0.0,
            "QueueLength_normal_ci_95": 0.0,
            "QueueLength_hist": np.zeros(SimResults.MAX_ENTRIES+1),
            "WaitingTime_all": deque(),
            "WaitingTime_mean": 0.0,
            "WaitingTime_std": 0.0,
            "WaitingTime_normal_ci_95": 0.0,
            "ServiceTime_mean": 0.0,
            "ServiceTime_std": 0.0,
            "ServiceTime_normal_ci_95": 0.0,
            "ServiceTime_all": deque(),
            "NCustomers_all": deque(),
            "NCustomers_mean": 0.0,
            "NCustomres_std": 0.0,
            "NCustomers_normal_ci_95": 0.0
        }

        q = queue_nr

        # iterate over all simulation runs 
        for i, simulation in enumerate(self.sim_runs):
            simulation = simulation[lam]
            
            # update statistics 
            statistics["QueueLengths_all"].append(
                simulation.get_mean_ql()[0][q]
            )
            statistics["WaitingTime_all"].append(
                simulation.get_mean_wait_t()[q][0]
            )
            statistics["QueueLength_hist"]+=simulation.get_ql_hist(queue_nr)
            
            statistics["ServiceTime_all"]+=simulation.S[q]
            statistics["NCustomers_all"].append(simulation.queueUsage[q])
            
        statistics["QueueLength_hist"] = statistics["QueueLength_hist"]/(i+1)

        # calculate mean and std 
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
        statistics["ServiceTime_mean"] = np.round(
            np.mean(statistics["ServiceTime_all"]), 3
        )
        statistics["ServiceTime_std"] = np.round(
            np.std(statistics["ServiceTime_all"]), 3
        )
        statistics["NCustomers_mean"] = np.round(
            np.mean(statistics["NCustomers_all"]), 3
        )
        statistics["NCustomers_std"] = np.round(
            np.std(statistics["NCustomers_all"]), 3
        )
        

        # calculate 95% confidence intervals
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

        statistics["ServiceTime_normal_ci_95"] = self.__ci_normal(
            self.nr_simulations,
            statistics["ServiceTime_mean"],
            statistics["ServiceTime_std"] ** 2,
            0.95,
        )
        
        statistics["NCustomers_normal_ci_95"] = self.__ci_normal(
            self.nr_simulations,
            statistics["NCustomers_mean"],
            statistics["NCustomers_std"] ** 2,
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

        logger.debug(
            f"Nr. of queues: {nr_queues}, nr. of servers: {nr_servers}",
            extra=self.logstr,
        )

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
            Distribution(stats.expon(scale=1/mu)) for mu in c.MU_ARRIVAL_RATE_SEC
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
        res = np.empty(len(self.arrival_time_dist), dtype = SimResults)
        
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
            assert (
                self.nr_servers % self.nr_queues == 0
            ), "Number of servers must be divisible by number of queues."
            nr_servers_per_queue = self.nr_servers // self.nr_queues
            logger.debug(
                f"Number of servers per queue: {nr_servers_per_queue}",
                extra=self.logstr,
            )

            for queue in self.queues:
                for s in range(nr_servers_per_queue):
                    queue.add_server(self.servers[s])

            # run simulation
            self.simulate_queue(dist)

            res[idx] = self.res
            
        return res

    def simulate_queue(self, dist) -> None:
        """
        Runs one full simulation.

        :return: The simulation results.
        """
        # debug variables to keep track of stuff
        n_arrivals = 0
        n_arrivals_groups = 0
        n_departures = 0
        
        N = 0 # number of customers in canteen 

        # initialize simulation
        fes = FES()
        self.res = SimResults(self.queues.size)
        t = 0
        
        # number of customers in canteen 
        N = 0 
        self.res.register_canteen(t, N)

        # create first group, update the FES with new arrival events
        # and intialize N as number of customers in canteen 
        fes = self.create_new_group(t_arr=t, fes=fes)

        # run simulation until t > SIM_T
        while t < c.SIM_T:
            # get queue lengths
            q_lengths = self.get_queue_lengths()
            self.res.register_queue_length(t, q_lengths)

            # get next event from FES
            e = fes.next()  # jump to next event
            t = e.time  # update time
            cust = e.get_customer()  # get customer

            logger.debug(f"Event: {e}", extra=self.logstr)

            # handle group arrival event 
            if e.type == Event.ARRIVAL_GROUP:
                n_arrivals_groups += 1 
                
                logger.debug(
                    f"--- ARRIVAL GROUP total: {n_arrivals_groups} ---",
                    extra=self.logstr,
                )
                
                # create new group and update the FES with new arrival events
                t_arr_new = t+dist.rvs(1)
                fes = self.create_new_group(t_arr=t_arr_new, fes=fes)
                
                N += e.get_customer().get_nr_customers()
                self.res.register_canteen(t, N)
            
            # handle customer arrival event
            elif e.type == Event.ARRIVAL:
                n_arrivals += 1
                logger.debug(
                    f"--- ARRIVAL total: {n_arrivals} ---", extra=self.logstr
                )

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
                
                # update number of customers through queue 
                self.res.register_queue_usage(q_id)

                # if there was a free server we schedule a departure event
                if self.queues[q_id].get_length() <= self.queues[q_id].get_n_servers():  # type: ignore
                    # get the server that will serve the customer
                    server = self.queues[q_id].get_server(server_id=0)  # type: ignore
                    t_service = server.get_service_time(
                        cust.get_uses_cash())*c.ADJUST_SERVICE[q_id]
                    self.res.register_service_time(t_service, q_id)
                    t_service += t 
                    
                    logger.debug(f"Scheduled new DEPARTURE {t_service}", extra=self.logstr)

                    # schedule departure event
                    dep_event = Event(Event.DEPARTURE, t_service, cust)
                    fes.add(dep_event)
                    cust.set_t_left(t_service)

                    # register waiting time 
                    self.res.register_waiting_time(t-cust.get_t_done_grab(), cust.get_queue_id())
                    
                    # register sojourn time 
                    self.res.register_sojourn_t(cust)

            # handle customer departure event
            elif e.type == Event.DEPARTURE:
                n_departures += 1
                logger.debug(
                    f"--- DEPARTURE total: {n_departures} ---",
                    extra=self.logstr,
                )
                # get the queue the customer is in and remove the customer from that queue
                q_id = cust.get_queue_id()
                self.queues[q_id].remove_customer(customer=cust, q_id=q_id)  # type: ignore
                
                # register number of customers in canteen 
                N -= 1 
                self.res.register_canteen(t, N)
                
                logger.debug(
                    f"Current number of customers in canteen: {N}",
                    extra = self.logstr,
                )

                # if there are customers waiting we schedule a departure event for the next customer
                nr_servers = self.queues[q_id].get_n_servers()  # type: ignore
                q_length = self.queues[q_id].get_length()  # type: ignore

                if q_length >= nr_servers:
                    logging.debug(
                        f"Queue {q_id} has more customers than servers",
                        extra=self.logstr,
                    )
                    # get the next customer in the queue
                    cust = self.queues[q_id].get_customer_at_pos(pos=nr_servers - 1)  # type: ignore

                    # get the server that will serve the customer
                    server = self.queues[q_id].get_server(server_id=0)  # type: ignore
                    t_service = server.get_service_time(
                        cust.get_uses_cash())*c.ADJUST_SERVICE[q_id]
                    self.res.register_service_time(t_service, q_id)
                    t_service += t 
                    
                    logger.debug(f"Scheduled new DEPARTURE {t_service}", extra=self.logstr)

                    # schedule departure event
                    dep_event = Event(Event.DEPARTURE, t_service, cust)
                    fes.add(dep_event)
                    cust.set_t_left(t_service)
                    
                    # register waiting time 
                    self.res.register_waiting_time(t-cust.get_t_done_grab(), cust.get_queue_id())
                    
                    # register sojourn time 
                    self.res.register_sojourn_t(cust)

            # log the FES / debug sleep
            if c.LOG_FES:
                logger.debug(f"FES: \n{fes}", extra=self.logstr)
            if c.DEBUG_THROTTLE is True:
                time.sleep(c.TIME_SLEEP)

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
        
        # register group 
        self.res.register_group(group)
        
        # add group arrival to FES
        fes.add(Event(Event.ARRIVAL_GROUP, t_arr, group))

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
