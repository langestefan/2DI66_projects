from scipy.stats import expon
import logging

from dist.distribution import Distribution

logger = logging.getLogger(__name__)


class Server:
    """Server class"""

    def __init__(self, id: int, mu_cash: float, mu_card: float):
        self.logstr = {"className": self.__class__.__name__}
        self.server_id = id  # unique id of the server
        self.mu_cash = mu_cash  # service time if customer pays with cash
        self.mu_card = mu_card  # service time if customer pays with card
        self.dist_cash = Distribution(expon(scale=mu_cash))
        self.dist_card = Distribution(expon(scale=mu_card))

    def __str__(self):
        return "Server id: " + str(self.get_id())

    def get_id(self):
        """
        Returns the ID of the server.
        """
        return self.server_id

    def get_service_time(self, cash: bool):
        """
        Returns the service time of the server.

        :param cash: Whether the customer uses cash to pay. If False, the
                     customer uses a bank card.

        :return: Service time of the server.
        """
        if cash:
            t_service = self.dist_cash.rvs(1)
        else:
            t_service = self.dist_card.rvs(1)

        logger.debug(f'Server {self.get_id()} service time: {round(t_service, 3)}', extra=self.logstr)
        return t_service
