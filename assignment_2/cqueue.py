from collections import deque
import logging

from assignment_2.customer import Customer
from assignment_2.server import Server

logger = logging.getLogger(__name__)


class CQueue:
    """We call it CQueue because Queue is already taken by the queue module."""

    def __init__(self, queue_id: int):
        self.logstr = {"className": self.__class__.__name__}
        self.queue = deque()
        self.queue_id = queue_id
        self.servers = []

    def __str__(self):
        return "Queue length: " + str(self.get_length())

    def add_customer(self, customer: Customer, q_id: int):
        """
        Adds a customer to the queue.

        :param customer: Customer to add.
        :param q_id: Queue ID to add customer to. Only used for sanity check.
        """
        if q_id != self.queue_id:
            raise ValueError("Queue ID does not match queue ID of queue.")

        self.queue.append(customer)
        queue_length = self.get_length()
        logger.debug(
            (
                f"Adding customer to queue: {self.queue_id}, new queue length:"
                f" {queue_length}"
            ),
            extra=self.logstr,
        )

    def get_customer_at_pos(self, pos: int):
        """
        Returns the customer at the front of the queue.

        :param pos: Position of customer in queue.

        :return: Customer at position pos in queue.
        """
        if self.get_length() < pos:
            raise ValueError(
                "Queue is not long enough to get customer at pos."
            )

        return self.queue[pos]

    def remove_customer(self, q_id: int, customer=None):
        """
        Removes a customer from the queue.

        :param q_id: Queue ID to add customer to. Only used for sanity check.
        :param customer: Customer to remove. Only used for sanity check. If None,
          we assume that the customer at the front of the queue is the one we want
        :return: Customer that was removed from queue.
        """
        if q_id != self.queue_id:
            raise ValueError("Queue ID does not match queue ID of queue.")

        queue_length = self.get_length()

        if queue_length == 0:
            raise ValueError("Cannot remove customer from empty queue.")
        logger.debug(
            (
                f"Removing customer from queue: {self.queue_id}, queue length:"
                f" {queue_length}"
            ),
            extra=self.logstr,
        )

        # remove customer from queue
        cust_front_q = self.queue.popleft()
        logger.debug(
            f"Removed customer from queue: {cust_front_q}", extra=self.logstr
        )

        # at this point popleft will give us the customer at the front of the queue
        # this customer must match the one we received from a DEPARTURE event
        if customer is not None:
            logger.debug(f"Comparing customer: {customer}", extra=self.logstr)

            # if there is one server per queue we have to sort by the arrival time
            # since that is the point int time they arrived in the queue
            # if there are multiple servers per queue we have to sort by the
            # departure time since that is the point in time they left the server
            if len(self.servers) == 1:
                t_front_q = cust_front_q.get_t_done_grab()  # arrival timestamp
                t_customer = customer.get_t_done_grab()  # arrival timestamp
                if t_front_q != t_customer:  # compare arrival timestamps
                    raise ValueError(
                        f"Customer ({t_front_q}) we want to remove is not the"
                        f" customer ({t_customer}) at the front of the queue."
                    )
            else:
                pass

        return cust_front_q

    def get_length(self):
        """
        Returns the length of the queue.

        :return: Length of queue.
        """
        queue_length = len(self.queue)
        if queue_length < 0:
            raise ValueError("Queue length cannot be negative.")
        return queue_length

    def add_server(self, server: Server):
        """
        Adds a server to the queue.

        :param server: Server to add.
        """
        self.servers.append(server)

    def get_n_servers(self):
        """
        Returns the number of servers in the queue.

        :return: Number of servers in queue.
        """
        return len(self.servers)

    def get_server(self, server_id: int):
        """
        Returns the server with the given ID.

        :param server_id: ID of server to return.
        :return: Server with given ID.
        """
        for server in self.servers:
            if server.get_id() == server_id:
                return server
        raise ValueError("Server with given ID does not exist.")
