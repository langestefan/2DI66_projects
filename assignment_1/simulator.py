from abc import ABC, abstractmethod
import multiprocessing as mp
from time import sleep

import assignment_1.constants as c
from assignment_1.game_state import GameState
from assignment_1.strategy import RandomStrategy


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
        self.game_history: GameHistory = GameHistory()
        self.parallelize = parallelize

    def get_game_history(self) -> GameHistory:
        """
        Returns the game history.

        :return: The game history.
        """
        if self.game_history is None:
            raise ValueError(
                "Game history is not initialized. Did you call"
                " start_simulation()?"
            )
        return self.game_history

    def run(self, n: int) -> None:
        """
        Starts the simulation.

        :param n: The number of simulation runs to perform.
        """
        # the results of the simulation runs will be written to the game history
        self.__do_n_runs(n, self.game_history, self.parallelize)

    def __do_n_runs(
        self,
        n: int,
        game_history: GameHistory,
        parallelize: bool = False,
    ) -> None:
        """
        Runs n simulations.

        :param n: The number of simulation runs to perform.
        :param parallelize: Whether to parallelize the simulation.
        """
        # if parallelization is enabled, use multiprocessing
        if parallelize:
            with mp.Pool() as pool:
                results = pool.map(self._do_one_run, range(n))  # type: ignore

                # add the results to the game history
                for result in results:
                    game_history.add_game_run(result)
        else:
            for i in range(n):
                result = self._do_one_run()
                game_history.add_game_run(result)

    @abstractmethod
    def _do_one_run(self) -> None:
        """
        Runs one game.
        """
        pass


class ChessSimulator(Simulator):
    """
    Implements the chess specific simulator.
    """

    def __init__(self):
        super().__init__()
        self.white_strat = RandomStrategy(player=c.Players.WHITE)
        self.black_strat = RandomStrategy(player=c.Players.BLACK)

    def _do_one_run(self) -> GameState:
        """
        Runs one full game from start to win/draw.

        :return: The final game state.
        """
        game_state = GameState()

        # run the game until it is over, then return the final game state obj
        while game_state.get_game_state() == c.GameStates.ONGOING:
            game_state.increment_round_number()
            if game_state.get_current_player() == c.Players.WHITE:
                print("White's turn")
                move = self.white_strat.get_move(game_state)
            else:
                print("Black's turn")
                move = self.black_strat.get_move(game_state)

            sleep(1)  # uncomment to slow down the simulation

            # start new round
            print(
                f"Starting new round with move {move} and player"
                f" {game_state.get_current_player()}"
            )
            game_state.start_new_round(move)

        return game_state
