import random
from abc import ABC, abstractmethod

import assignment_1.constants as c


class Strategy(ABC):
    def __init__(self, player):
        self.player: int = player

    @abstractmethod
    def get_move(self):
        pass


class RandomStrategy(Strategy):
    def __init__(self, player):
        super().__init__(player)

    def get_move(self, board):
        possible_moves = []

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == self.player:
                    possible_moves.append((i, j))

        return random.choice(possible_moves)
