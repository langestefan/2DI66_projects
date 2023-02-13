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


class Simulator(ABC):
    """
    A base class to represent a simulator.
    """

    def __init__(self, parallelize: bool, n_jobs: int):
        super().__init__()
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
        self.white_strat = RandomStrategy(player=c.Players.WHITE)
        self.black_strat = RandomStrategy(player=c.Players.BLACK)

    def _do_one_run(self, n: int) -> GameState:
        game_state = GameState()

        # run the game until it is over, then return the final game state obj
        while game_state.get_game_state() == c.GameStates.ONGOING:
            print("\n-------------------------------------------------\n")
            # increment the round number
            game_state.increment_round_number()
            print(
                f"Round: {game_state.get_round_number()}; "
                f"Player: {game_state.get_current_player()}"
            )

            if game_state.get_current_player() == c.Players.WHITE:
                print("White's turn")
                move = self.white_strat.get_move(game_state)
            else:
                print("Black's turn")
                move = self.black_strat.get_move(game_state)

            # move is none, game is over so we break the loop
            if move is None:
                break
            
            print(f"Player {game_state.get_current_player()} moved {move[0], move[1]} to {move[2], move[3]}")
            if game_state.chess_board.board[move[0], move[1]].name == 'Pawn' and move[2]%4 == 0: 
                print(f"Player {game_state.get_current_player()} promoted pawn to queen at {move[2], move[3]}")
            

            # start new round
            game_state.start_new_round(move)
        # print final board state
        print(f"Final board state: \n{game_state.get_board()}")
        return game_state
