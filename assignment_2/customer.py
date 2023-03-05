import logging

logger = logging.getLogger(__name__)


class Customer:
    def __init__(self, t_arr: float, cash: bool = False):
        """
        Creates a new customer.

        :param t_arr: The time the customer arrived.
        :param cash: Whether the customer uses cash to pay. If False, the
                     customer uses a bank card.
        """
        self.logstr = {"className": self.__class__.__name__}
        self.t_arrival = t_arr
        self.use_cash = cash

    def __str__(self):
        return (
            "Customer at: "
            + str(self.t_arrival)  # noqa: W503
            + " with cash: "  # noqa: W503
            + str(self.use_cash)  # noqa: W503
        )
