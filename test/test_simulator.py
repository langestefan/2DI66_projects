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
