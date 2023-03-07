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
        self.t_arrival = t_arr
        self.t_grab_food = t_grab_food

        # time when done grabbing food
        self.t_done_grab_food = t_arr + t_grab_food

    def __str__(self):
        return (
            "Customer at: "
            + str(self.t_arrival)  # noqa: W503
            + " with cash: "  # noqa: W503
            + str(self.use_cash)  # noqa: W503
        )

    def get_time_done_grab_food(self):
        """
        Returns the time the customer is done grabbing their food.

        :return: Time stamp of done grabbing food.
        """
        return self.t_done_grab_food
