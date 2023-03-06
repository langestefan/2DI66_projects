import pytest

# to enable parent directory imports
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from assignment_2.group import Group


t_arrival = 0
group_size = 5


class TestGroup:
    @pytest.fixture(autouse=True)
    def create_group(self):
        """
        Creates a chess board object
        """

        return Group(t_arr=t_arrival, N=group_size)

    def test_group_creation(self, create_group):
        """
        Tests if the group is created correctly.
        """
        assert create_group is not None
        assert create_group.t_arrival == t_arrival
        assert create_group.n_customers == group_size
