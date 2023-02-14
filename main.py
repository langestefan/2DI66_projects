import multiprocessing as mp

from assignment_1.simulator import ChessSimulator

import logging


if __name__ == "__main__":
    n_jobs = mp.cpu_count() // 2
    parallelize = True
    n_games = 100

    # Start logging
    logger = logging.getLogger(__name__)
    logger.info(
        f"Starting simulator with {n_jobs} jobs, parallelize={parallelize}",
        extra={"className": ""},
    )

    # Create a simulator.
    simulator = ChessSimulator(parallelize=True, n_jobs=n_jobs)

    # Run the simulator.
    simulator.run(n=n_games)

    # Get game history.
    game_history = simulator.get_game_history()

    # Print statistics.
    statistics = game_history.get_statistics()

    str = "\n\nStatistics:\n\n"
    for key, value in statistics.items():
        str += f"{key}: {value}\n"
    logger.info(str, extra={"className": ""})
