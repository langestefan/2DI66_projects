import logging

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

    def __str__(self):
        return (
            "Group at: "
            + str(self.t_arrival)  # noqa: W503
            + " with N: "  # noqa: W503
        )
