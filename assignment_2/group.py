import logging
import scipy.stats as stats

import assignment_2.constants as c
import assignment_2.customer as Customer

logger = logging.getLogger(__name__)


class Group:
    def __init__(self, t_arr: float, N: int):
        """
        Creates a new group of customers.

        :param t_arr: The time the group arrived.
        :param N: The number of customers in the group.

        """
        self.logstr = {"className": self.__class__.__name__}
        self.t_arrival = t_arr
        self.n_customers = N

        # list of customers
        self.customers = []

        # add customers to the group
        for i in range(N):
            use_cash = stats.bernoulli.rvs(c.P_CASH)
            self.customers.append(Customer.Customer(t_arr, bool(use_cash)))

    def __str__(self):
        return (
            "Group at: "
            + str(self.t_arrival)  # noqa: W503
            + " with N: "  # noqa: W503
        )

    def add_customer(self, customer):
        """
        Adds a customer to the group.

        :param customer: The customer to add.
        """
        self.customers.append(customer)
