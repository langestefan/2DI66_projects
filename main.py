import multiprocessing as mp
import time

from assignment_1.simulator import ChessSimulator
from assignment_1.strategy import RandomStrategy
import assignment_1.constants as c

import logging


if __name__ == "__main__":
    n_jobs = mp.cpu_count() - 1
    parallelize = True
    n_games = 1000

    # Start logging
    logger = logging.getLogger(__name__)
    logger.info(
        f"Starting simulator with {n_jobs} jobs, parallelize={parallelize}",
        extra={"className": ""},
    )

    # Create a simulator.
    black_strategy = RandomStrategy(
        player=c.Players.BLACK, allow_two_step_pawn=False
    )
    white_strategy = RandomStrategy(
        player=c.Players.WHITE, allow_two_step_pawn=True
    )

    simulator = ChessSimulator(
        parallelize=True,
        n_jobs=n_jobs,
        black_strat=black_strategy,
        white_strat=white_strategy,
    )

    # Run the simulator.
    start_time = time.time()
    simulator.run(n=n_games)

    # Print time
    st_str = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    logger.info(f"Simulator finished in {st_str}", extra={"className": ""})

    # Get game history.
    game_history = simulator.get_game_history()

    # Print statistics.
    statistics = game_history.get_statistics()

    str = "\n\nStatistics:\n\n"
    for key, value in statistics.items():
        str += f"{key}: {value}\n"
    logger.info(str, extra={"className": ""})
