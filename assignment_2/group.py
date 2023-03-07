import logging
import numpy as np

import assignment_2.customer as Customer

logger = logging.getLogger(__name__)


class Group:
    def __init__(
        self,
        n_customers: int,
        use_cash: np.ndarray,
        t_arr: float,
        t_grab_food: np.ndarray,
    ):
        """
        Creates a new group of customers.

        :param n_customers: The number of customers in the group.
        :param use_cash: A list of booleans indicating whether the customer uses cash or not.
        :param t_arr: The time the group arrived.
        :param t_grab_food: A list of times the customers need to grab their food.
        """
        self.logstr = {"className": self.__class__.__name__}
        self.t_arrival = t_arr
        self.n_customers = n_customers

        if len(t_grab_food) != n_customers or len(use_cash) != n_customers:
            raise ValueError(
                "Nr of customers and nr grab food times do not match."
            )

        # list of customers
        self.customers = np.empty(n_customers, dtype=Customer.Customer)

        # add customers to the group
        for idx, use_cash_cust in enumerate(use_cash):
            self.customers[idx] = Customer.Customer(
                t_arr=t_arr,
                t_grab_food=t_grab_food[idx],
                cash=use_cash_cust,
            )

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
