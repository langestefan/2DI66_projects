import pytest

# to enable parent directory imports
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from assignment_2.customer import Customer

t_arr = 1.2
t_grab_dt = 5.4
t_grab = t_arr + t_grab_dt
use_cash = True


class TestGroup:
    @pytest.fixture(autouse=True)
    def create_customer(self):
        """
        Creates a chess board object
        """

        return Customer(t_arr, t_grab, use_cash)

    def test_customer_creation(self, create_customer):
        """
        Tests if the group is created correctly.
        """
        assert create_customer is not None
        assert create_customer.get_t_done_grab() == t_grab

    def test_t_grab_food_lt_t_arr(self):
        """
        Tests if we get a value error if t_grab_food < t_arr.
        """
        t_grab_lt = 1.0
        t_arr_lt = 2.0

        with pytest.raises(ValueError):
            Customer(t_arr_lt, t_grab_lt, use_cash)

    def test_t_grab_food_eq_t_arr(self):
        """
        Tests if we get a value error if t_grab_food == t_arr.
        """
        t_grab_eq = 1.0
        t_arr_eq = 1.0

        with pytest.raises(ValueError):
            Customer(t_arr_eq, t_grab_eq, use_cash)
