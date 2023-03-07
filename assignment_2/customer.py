import logging
import scipy.stats as stats
from dist.distribution import Distribution

import assignment_2.constants as c


logger = logging.getLogger(__name__)


class Customer:
    def __init__(self, t_arr: float, t_grab_food: float, cash: bool):
        """
        Creates a new customer.

        :param t_arr: The time the customer arrived.
        :param t_grab_food: The time the customer needs to grab their food.
        :param cash: Whether the customer uses cash to pay. If False, the
                     customer uses a bank card.
        """
        self.logstr = {"className": self.__class__.__name__}
        self.use_cash = cash
        self.t_arrival_group = t_arr
        self.t_grab_food = t_grab_food

        # make sure t_grab_food > t_arrival_group
        if t_grab_food <= t_arr:
            raise ValueError("t_grab_food <= t_arr")

    def __str__(self):
        return (
            "with cash: "  # noqa: W503
            + str(self.use_cash)  # noqa: W503
        )

    def get_t_done_grab(self):
        """
        Returns the time the customer is done grabbing their food.

        :return: Time stamp of done grabbing food.
        """
        return self.t_grab_food
