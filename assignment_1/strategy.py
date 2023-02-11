import numpy as np
import random
import copy
from abc import ABC, abstractmethod

import assignment_1.constants as c
import assignment_1.pieces as p
from assignment_1.game_state import GameState


class Strategy(ABC):
    def __init__(self, player: c.Players):
        self.player: c.Players = player
        self.move_history: list = []

    @abstractmethod
    def get_move(self, game_state: GameState):
        """
        Returns the move the strategy wants to make for a given board state
        and a given player.
        :param board: The current board state.
        :param player: The player for which the move is made.
        :return: The move the strategy wants to make.
        """
        pass

    def get_valid_moves(self, game_state: GameState):
        """Checks which moves are valid for the player.
        :param board: The current board state.
        :return: A list of valid moves for the player.
        """
        if type(game_state) is not GameState:
            raise TypeError("game_state must be of type GameState.")

        board_arr = game_state.get_board().get_board_arr()

        # we will initialize the array with -1, so we can filter valid moves
        # format: [from_x, from_y, to_x, to_y]
        valid_moves = np.ones((100, 4), dtype=int) * -1

        # go over all pieces of the player and get valid moves
        move_index: int = 0
        for i in range(c.BOARD_SIZE):
            for j in range(c.BOARD_SIZE):
                piece = board_arr[i, j]  # type: ignore

                # some sanity checks
                if piece is not None and piece.get_player() == self.player:
                    pos_piece = piece.get_position()
                    pos_array = np.array([i, j])
                    if not (pos_piece == pos_array).all():
                        raise ValueError(
                            "Piece position does not match board position."
                        )

                    moves = piece.get_valid_moves(board_arr)
                    valid_moves[move_index : move_index + len(moves)] = moves
                    move_index += len(moves)

        # filter out invalid moves
        valid_moves = valid_moves[valid_moves[:, 0] != -1]
        return valid_moves


class RandomStrategy(Strategy):
    def __init__(self, player: c.Players):
        super().__init__(player)

    def get_move(self, game_state: GameState):
        if type(game_state) is not GameState:
            raise TypeError("game_state must be of type GameState.")

        # get a list of valid moves
        valid_moves = super().get_valid_moves(game_state)

        # randomly select a move
        n_moves = len(valid_moves)

        # no valid moves: king is in checkmate or draw
        if n_moves == 0:
            move = np.ndarray((1, 4), dtype=int)
            move.fill(-1)
            return move

        # randomly select a move, uniform distribution
        random_move = valid_moves[random.randint(0, n_moves - 1)]
        return random_move
