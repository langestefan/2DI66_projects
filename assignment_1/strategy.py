import numpy as np
import random
from abc import ABC, abstractmethod

import assignment_1.constants as c
from assignment_1.game_state import GameState


class Strategy(ABC):
    def __init__(self, player: c.Players, allow_two_step_pawn: bool):
        self.player: c.Players = player
        self.move_history: list = []
        self.allow_two_step_pawn: bool = allow_two_step_pawn

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


# TODO: implement allow_two_step_pawn enable/disable


class RandomStrategy(Strategy):
    def __init__(self, player: c.Players, allow_two_step_pawn: bool = True):
        super().__init__(player, allow_two_step_pawn)

    def get_move(self, game_state: GameState):
        if type(game_state) is not GameState:
            raise TypeError("game_state must be of type GameState.")

        # get a list of valid moves
        valid_moves = game_state.get_valid_moves(self.player)

        # randomly select a move
        n_moves = len(valid_moves)

        # no valid moves: king is in checkmate or draw
        if n_moves == 0:
            print("No valid moves!")

            # no valid moves, checkmate or draw?
            king_in_check = game_state.king_is_in_check(self.player)
            if king_in_check:
                print(f"King of player {self.player} is in check!")

            # checkmate
            if king_in_check:
                if self.player == c.Players.WHITE:
                    print("Black wins!")
                    game_state.set_game_state(c.GameStates.BLACK_WON)
                else:
                    print("White wins!")
                    game_state.set_game_state(c.GameStates.WHITE_WON)
            # draw
            else:
                print("Draw!")
                game_state.set_game_state(c.GameStates.DRAW)
            return None

        # randomly select a move, uniform distribution
        random_move = valid_moves[random.randint(0, n_moves - 1)]
        return random_move
