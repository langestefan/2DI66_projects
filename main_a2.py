import logging
import os
import multiprocessing as mp
import time

# custom imports
import assignment_2.simulator as sim
import assignment_2.constants as c
import assignment_2.analysis as analysis
import matplotlib.pyplot as plt

logging.basicConfig(
    level=c.LOG_LEVEL,
    format=(
        "[%(asctime)s] %(levelname)s [%(name)s::%(className)s:%(lineno)s]"
        " %(message)s"
    ),
)

os.system("")
logging.getLogger("numexpr").setLevel(logging.WARNING)

# Close all open plots
plt.close("all")

# Create a folder for the simulation results
CURRENT_TIME = time.strftime("%Y%m%d-%H%M")
SIM_PATH = os.path.join("sims", CURRENT_TIME)
if not os.path.exists(SIM_PATH):
    os.makedirs(SIM_PATH)
time.sleep(3)


if __name__ == "__main__":
    n_jobs = mp.cpu_count()
    n_sims = 5000

    # Start logging
    logger = logging.getLogger(__name__)
    logger.info(
        f"Starting simulator with {n_jobs} jobs",
        extra={"className": ""},
    )

    # Create a simulator.
    simulator = sim.QueueSimulator(
        n_jobs=n_jobs, nr_queues=c.N_QUEUES, nr_servers=c.N_SERVERS
    )

    # Run the simulator.
    simulator.run(n=n_sims)

    # Get the results.
    results = simulator.get_sim_history()

    # Save some results
    analysis.save_files(results, n_sims)

    # Plot results
    # some parameters that can be defined (lam = index of rate parameter)
    binwidth = 10
    time_interval = 50

    for lam in range(len(c.MU_ARRIVAL_RATE_MIN)):
        if lam < 3:
            # all queues together
            analysis.plot_QL_hist_all(results, lam, maxq=50, path=SIM_PATH)
        else:
            # all queues together
            analysis.plot_QL_hist_all(results, lam, maxq=75, path=SIM_PATH)

        # queues separated
        analysis.plot_QL_hist_per_queue(results, lam, maxq=50, path=SIM_PATH)

        # all queues together
        analysis.plot_hist_wait_t_all(
            results, lam, binwidth=binwidth, path=SIM_PATH
        )

        # queues separated
        analysis.plot_hist_wait_t_per_queue(
            results, lam, binwidth=binwidth, path=SIM_PATH
        )

        # means of customers in canteen
        analysis.plot_hist_cust_in_cant(
            results, lam, binwidth=binwidth, path=SIM_PATH
        )

        # nr customers in canteen vs time (moving average)
        analysis.plot_hist_CC_vs_time(
            results, lam, time_interval=time_interval, path=SIM_PATH
        )

    logger.info(
        f"Ending simulator with {n_jobs} jobs",
        extra={"className": ""},
    )
