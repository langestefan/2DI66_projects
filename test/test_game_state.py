import pytest
import numpy as np

import assignment_1.constants as c
from assignment_1.game_state import GameState


class TestClientGameState:
    @pytest.fixture(autouse=True)
    def create_game_state(self):
        """
        Creates a game state object.
        """
        return GameState()

    def test_game_state_creation(self, create_game_state):
        """
        Tests if the game state object is created correctly.
        """
        assert create_game_state is not None
        assert create_game_state.get_round_number() == -1
        create_game_state.start_new_round(move=np.array([4, 4, 2, 2]))
        assert create_game_state.get_current_player() == c.Players.WHITE

    def test_game_state_start_new_round(self, create_game_state):
        """
        Tests if the round number is incremented correctly.
        """
        create_game_state.increment_round_number()
        create_game_state.start_new_round(move=np.array([4, 4, 2, 2]))
        assert create_game_state.get_current_player() == c.Players.WHITE
        create_game_state.increment_round_number()
        create_game_state.start_new_round(move=np.array([0, 0, 2, 3]))
        assert create_game_state.get_round_number() == 1
        assert create_game_state.get_current_player() == c.Players.BLACK
