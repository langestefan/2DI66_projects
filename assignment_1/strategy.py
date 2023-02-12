import numpy as np
import random
from abc import ABC, abstractmethod

import assignment_1.constants as c
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


class RandomStrategy(Strategy):
    def __init__(self, player: c.Players):
        super().__init__(player)

    def get_move(self, game_state: GameState):
        if type(game_state) is not GameState:
            raise TypeError("game_state must be of type GameState.")

        # first we check if our king is in check by checking opponent's valid moves
        opponent = c.Players((self.player.value + 1) % 2)
        valid_moves = game_state.get_valid_moves(opponent)
        king_in_check = game_state.king_is_in_check(self.player, valid_moves)
        if king_in_check:
            print(f'King of player {self.player} is in check!')

        # get a list of valid moves
        valid_moves = game_state.get_valid_moves(self.player)

        # randomly select a move
        n_moves = len(valid_moves)

        # no valid moves: king is in checkmate or draw
        if n_moves == 0:
            print("No valid moves!")
            if king_in_check:
                if self.player == c.Players.WHITE:
                    print("Black wins!")
                    game_state.set_game_state(c.GameStates.BLACK_WON)
                else:
                    print("White wins!")
                    game_state.set_game_state(c.GameStates.WHITE_WON)
            else:
                print("Draw!")
                game_state.set_game_state(c.GameStates.DRAW)
            return None

        # randomly select a move, uniform distribution
        random_move = valid_moves[random.randint(0, n_moves - 1)]
        return random_move
