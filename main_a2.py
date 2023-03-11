import logging
import os
import multiprocessing as mp
import pickle

# custom imports
import assignment_2.simulator as sim
import assignment_2.constants as c
import assignment_2.analysis as analysis 

logging.basicConfig(
    level=c.LOG_LEVEL,
    format=(
        "[%(asctime)s] %(levelname)s [%(name)s::%(className)s:%(lineno)s]"
        " %(message)s"
    ),
)
    
os.system("")
logging.getLogger('numexpr').setLevel(logging.WARNING)

import matplotlib.pyplot as plt 
plt.close('all')


if __name__ == "__main__":
    n_jobs = mp.cpu_count() - 2
    n_sims = 10000

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
            analysis.plot_QL_hist_all(results, lam, maxq=50) # all queues together 
        else:
            analysis.plot_QL_hist_all(results, lam, maxq=75) # all queues together 
        
        analysis.plot_QL_hist_per_queue(results, lam, maxq=50) # queues separated 
        analysis.plot_hist_wait_t_all(results, lam, binwidth) # all queues together
        analysis.plot_hist_wait_t_per_queue(results, lam, binwidth) # queues separated
        analysis.plot_hist_cust_in_cant(results, lam, binwidth) # means of customers in canteen
        analysis.plot_hist_CC_vs_time(results, lam, time_interval) # nr customers in canteen vs time (moving average)
    
    logger.info(
        f"Ending simulator with {n_jobs} jobs",
        extra={"className": ""},    
    )
    
        

    