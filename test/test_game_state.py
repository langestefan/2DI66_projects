from conftest import Context as ctx
import assignment_1.constants as c

import pytest



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
        assert create_game_state.get_round_number() == 0
        assert create_game_state.get_player() == c.PLAYER_WHITE

    def test_game_state_start_new_round(self, create_game_state):
        """
        Tests if the round number is incremented correctly.
        """
        create_game_state.start_new_round()
        assert create_game_state.get_round_number() == 1
        assert create_game_state.get_player() == c.PLAYER_BLACK
