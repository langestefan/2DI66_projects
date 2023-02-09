import numpy as np
from abc import ABC, abstractmethod
import multiprocessing as mp
from functools import partial

import assignment_1.constants as c
from assignment_1.game_state import GameState


class GameHistory:
    """
    This class is used to store the history of games played. It contains a list
    of game runs, the winner of each game and the number of games played. One
    game run is one finished game. When a game is finished, the final GameState
    is appended to the list of game runs.
    """

    def __init__(self):
        self.game_runs: list[GameState] = []
        self.games_played = 0

    def add_game_run(self, game_run):
        """
        Adds a game run to the game runs.

        :param game_run: The game run to be added.
        """
        self.game_runs.append(game_run)
        self.games_played += 1

    def get_game_runs(self) -> list:
        """
        Returns the list containing all game runs.

        :return: The game runs.
        """
        return self.game_runs

    def get_number_of_games_played(self) -> int:
        """
        Returns the number of games played.

        :return: The number of games played.
        """
        return self.games_played


class Simulator(ABC):
    """
    A base class to represent a simulator.
    """

    def __init__(self, parallelize: bool = False):
        super().__init__()
        self.game_history = None
        self.parallelize = parallelize

    def get_game_history(self) -> GameHistory:
        """
        Returns the game history.

        :return: The game history.
        """
        return self.game_history

    def start_simulation(self, n: int) -> None:
        """
        Starts the simulation.

        :param n: The number of simulation runs to perform.
        """
        self.game_history = GameHistory()
        self.__do_n_runs(n, self.parallelize)

    def __do_n_runs(self, n: int, parallelize: bool = False) -> None:
        """
        Runs n simulations.

        :param n: The number of simulation runs to perform.
        :param parallelize: Whether to parallelize the simulation.
        """
        if parallelize:
            results = self.__do_n_runs_parallel(n)
        else:
            results = self.__do_n_runs_sequential(n)

        return results

    def __do_n_runs_parallel(self, n: int) -> None:
        """
        Runs n simulations in parallel.

        :param n: The number of simulation runs to perform.

        :return: A list of results.
        """
        results = []
        with mp.Pool() as pool:
            results = pool.map(self.do_one_run, range(n))
        return results

    def __do_n_runs_sequential(self, n: int) -> None:
        """
        Runs n simulations sequentially.

        :param n: The number of simulation runs to perform.

        :return: A list of results.
        """
        results = []
        for i in range(n):
            results.append(self.do_one_run())
        return results

    @abstractmethod
    def do_one_run(self) -> None:
        """
        Runs one game.
        """
        pass


class ChessSimulator(Simulator):
    """
    Implements the chess specific simulator.
    """

    def __init__(self):
        self.game_history = GameHistory()

    def do_one_run(self) -> GameState:
        """
        Runs one game.

        :return: The final game state.
        """
        game_state = GameState()
        while game_state.get_game_state() == c.game_states["ongoing"]:
            game_state = game_state.get_next_state()

        self.game_history.add_game_run(game_state)
        return game_state
