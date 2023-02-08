from conftest import Context as ctx
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
