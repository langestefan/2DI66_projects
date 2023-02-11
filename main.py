import multiprocessing as mp

from assignment_1.simulator import ChessSimulator


if __name__ == "__main__":
    simulator = ChessSimulator(parallelize=True, n_jobs=mp.cpu_count() // 2)

    # Run the simulator.
    simulator.run(n=500)

    # Print the game history.
    print(simulator.get_game_history())
