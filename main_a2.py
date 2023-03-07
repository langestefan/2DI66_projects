import multiprocessing as mp
import logging
import os

# custom imports
import assignment_2.simulator as sim
import assignment_2.constants as c

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        "[%(asctime)s] %(levelname)s [%(name)s::%(className)s:%(lineno)s]"
        " %(message)s"
    ),
)

os.system("")


if __name__ == "__main__":
    n_jobs = 1  # mp.cpu_count() - 1
    n_sims = 1

    # Start logging
    logger = logging.getLogger(__name__)
    logger.info(
        f"Starting simulator with {n_jobs} jobs",
        extra={"className": ""},
    )

    # Create a simulator.
    simulator = sim.QueueSimulator(n_jobs=n_jobs, nr_queues=c.N_QUEUES, nr_servers=c.N_SERVERS)

    # Run the simulator.
    simulator.run(n=n_sims)

    # # Get the results.
    # results = simulator.get_results()
