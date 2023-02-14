from abc import ABC, abstractmethod
import multiprocessing as mp
import numpy as np

import assignment_1.constants as c
from assignment_1.game_state import GameState
from assignment_1.strategy import RandomStrategy

import logging

logging.basicConfig(
    level=logging.INFO,
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


class GameHistory:
    """
    This class is used to store the history of games played. It contains a list
    of game runs, the winner of each game and the number of games played. One
    game run is one finished game. When a game is finished, the final GameState
    is appended to the list of game runs.
    """

    def __init__(self):
        self.logstr = {"className": self.__class__.__name__}
        self.game_runs: list[GameState] = []
        self.games_played = 0

    def __str__(self):
        str = f"Number of games played: {self.games_played}"

        for game_run in self.game_runs:
            str += f"\n Final game state: {game_run.get_game_state()}"
            str += f"\n Round number: {game_run.get_round_number()}"

        return str

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

    def get_statistics(self) -> dict:
        """
        Computes the statistics of the game results.

        :return: Dictionary with statistics.
        """

        statistics = {
            c.GameStates.WHITE_WON: 0,
            c.GameStates.BLACK_WON: 0,
            c.GameStates.DRAW: 0,
            "white_wins_prop": 0.0,
            "black_wins_prop": 0.0,
            "draws_prop": 0.0,
            "games_played": 0,
            "white_wins_ci_99": 0.0,
            "black_wins_ci_99": 0.0,
            "draws_ci_99": 0.0,
            "white_wins_ci_95": 0.0,
            "black_wins_ci_95": 0.0,
            "draws_ci_95": 0.0,
            "mean_rounds_per_game": 0.0,
            "mean_rounds_per_game_ci_99": 0.0,
            "mean_rounds_per_game_ci_95": 0.0,
            "n_games_queen_promoted": 0,
            "n_games_queen_promoted_prop": 0.0,
            "n_games_queen_promoted_ci_99": 0.0,
            "n_games_queen_promoted_ci_95": 0.0,
        }

        # go over all final game states and compute the statistics
        round_numbers = np.ones(self.games_played) * -1
        n_games_queen_promoted = 0

        for i, game_run in enumerate(self.game_runs):
            final_state = game_run.get_game_state()
            statistics[final_state] += 1
            round_numbers[i] = game_run.get_round_number()
            n_games_queen_promoted += game_run.game_had_queen_promoted()

        # compute the proportions of the game results
        n = self.games_played
        p_white = statistics[c.GameStates.WHITE_WON] / n
        p_black = statistics[c.GameStates.BLACK_WON] / n
        p_draw = statistics[c.GameStates.DRAW] / n
        statistics["white_wins_prop"] = np.round(p_white, 3)
        statistics["black_wins_prop"] = np.round(p_black, 3)
        statistics["draws_prop"] = np.round(p_draw, 3)
        statistics["games_played"] = n

        # statistics for queen promotion
        p_queen_promoted = n_games_queen_promoted / n
        statistics["n_games_queen_promoted"] = n_games_queen_promoted
        statistics["n_games_queen_promoted_prop"] = np.round(
            p_queen_promoted, 3
        )
        statistics["n_games_queen_promoted_ci_99"] = self.__ci_binomial(
            n, p_queen_promoted, 0.99
        )
        statistics["n_games_queen_promoted_ci_95"] = self.__ci_binomial(
            n, p_queen_promoted, 0.95
        )

        # compute statistics for game result proportions
        statistics["white_wins_ci_99"] = self.__ci_binomial(n, p_white, 0.99)
        statistics["black_wins_ci_99"] = self.__ci_binomial(n, p_black, 0.99)
        statistics["draws_ci_99"] = self.__ci_binomial(n, p_draw, 0.99)
        statistics["white_wins_ci_95"] = self.__ci_binomial(n, p_white, 0.95)
        statistics["black_wins_ci_95"] = self.__ci_binomial(n, p_black, 0.95)
        statistics["draws_ci_95"] = self.__ci_binomial(n, p_draw, 0.95)

        # compute statistics for mean number of rounds per game
        statistics["mean_rounds_per_game"] = np.round(
            np.mean(round_numbers), 3
        )
        statistics["mean_rounds_per_game_ci_99"] = self.__ci_normal(
            n, np.mean(round_numbers), np.var(round_numbers), 0.99
        )
        statistics["mean_rounds_per_game_ci_95"] = self.__ci_normal(
            n, np.mean(round_numbers), np.var(round_numbers), 0.95
        )

        return statistics

    def __ci_binomial(self, n: int, p: float, alpha: float) -> tuple:
        """
        Computes the confidence interval for a binomial distribution.

        :param n: The number of trials.
        :param p: The probability of success.
        :param alpha: The significance level.
        :return: The confidence interval.
        """

        # assume a binomial distribution and compute the confidence interval
        z = conf_to_z[alpha]
        p_up = np.round(p + z * np.sqrt(p * (1 - p) / n), 3)
        p_low = np.round(p - z * np.sqrt(p * (1 - p) / n), 3)

        # return the confidence interval
        return (p_low, p_up)

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

    def __init__(self, parallelize: bool, n_jobs: int):
        super().__init__()
        self.logstr = {"className": self.__class__.__name__}
        self.game_history: GameHistory = GameHistory()
        self.parallelize = parallelize
        self.n_jobs: int = n_jobs

    def get_game_history(self) -> GameHistory:
        """
        Returns the game history.

        :return: The game history.
        """
        if self.game_history is None:
            raise ValueError(
                "Game history is not initialized. Did you call run()?"
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
            with mp.Pool(processes=self.n_jobs) as pool:
                results = pool.map(self._do_one_run, range(n))

                # add the results to the game history
                for result in results:
                    game_history.add_game_run(result)
        else:
            for i in range(n):
                result = self._do_one_run(i)
                game_history.add_game_run(result)

    @abstractmethod
    def _do_one_run(self, n: int) -> GameState:
        """
        Runs one game.

        :param n: The number of the game run.
        """
        pass


class ChessSimulator(Simulator):
    """
    Implements the chess specific simulator.
    """

    def __init__(self, parallelize: bool = False, n_jobs: int = 1):
        super().__init__(parallelize=parallelize, n_jobs=n_jobs)
        self.white_strat = RandomStrategy(
            player=c.Players.WHITE, allow_two_step_pawn=False
        )
        self.black_strat = RandomStrategy(
            player=c.Players.BLACK, allow_two_step_pawn=False
        )

    def _do_one_run(self, n: int) -> GameState:
        game_state = GameState()

        # run the game until it is over, then return the final game state obj
        while game_state.get_game_state() == c.GameStates.ONGOING:
            # increment the round number
            game_state.increment_round_number()
            logger.debug(
                (
                    f"Round: {game_state.get_round_number()}; "
                    f"Player: {game_state.get_current_player()}"
                ),
                extra=self.logstr,
            )

            if game_state.get_current_player() == c.Players.WHITE:
                move = self.white_strat.get_move(game_state)
            else:
                move = self.black_strat.get_move(game_state)

            # move is none, game is over so we break the loop
            if move is None:
                break

            logger.debug(
                (
                    f"Player {game_state.get_current_player()} moved"
                    f" {move[0], move[1]} to {move[2], move[3]}"
                ),
                extra=self.logstr,
            )
            if (
                game_state.chess_board.board[move[0], move[1]].name == "Pawn"  # type: ignore
                and move[2] % 4 == 0
            ):
                logger.debug(
                    (
                        f"Player {game_state.get_current_player()} promoted"
                        f" pawn to queen at {move[2], move[3]}"
                    ),
                    extra=self.logstr,
                )

            # start new round
            game_state.start_new_round(move)

        # log final board state
        logger.debug(
            f"Final board state: \n{game_state.get_board()}", extra=self.logstr
        )
        return game_state
