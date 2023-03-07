import pytest
import numpy as np

# to enable parent directory imports
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from assignment_2.group import Group


t_arr = 8.4
n_customers = 5
use_cash = np.array([True, True, True, False, False], dtype=bool)
t_grab = np.array([5.1, 10.4, 15.3, 20.2, 25.4], dtype=float) + t_arr


class TestGroup:
    @pytest.fixture(autouse=True)
    def create_group(self):
        """
        Creates a chess board object
        """

        return Group(n_customers, use_cash, t_arr, t_grab)

    def test_group_creation(self, create_group):
        """
        Tests if the group is created correctly.
        """
        assert create_group is not None
        assert create_group.get_nr_customers() == n_customers
        assert len(create_group.get_customers()) == n_customers

    def test_t_grab_food_lt_t_arr(self):
        """
        Tests if we get a value error if t_grab_food < t_arr.
        """
        t_grab_lt = np.ones(n_customers, dtype=float)
        t_arr_lt = 10.0

        with pytest.raises(ValueError):
            Group(n_customers, use_cash, t_arr_lt, t_grab_lt)

    def test_t_grab_food_eq_t_arr(self):
        """
        Tests if we get a value error if t_grab_food == t_arr.
        """
        t_grab_eq = np.ones(n_customers, dtype=float)
        t_arr_eq = 1.0

        with pytest.raises(ValueError):
            Group(n_customers, use_cash, t_arr_eq, t_grab_eq)
