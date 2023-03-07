from collections import deque
import logging

from assignment_2.customer import Customer

logger = logging.getLogger(__name__)


class CQueue:
    """We call it CQueue because Queue is already taken by the queue module."""

    def __init__(self, queue_id: int):
        self.logstr = {"className": self.__class__.__name__}
        self.queue = deque()
        self.queue_id = queue_id

    def __str__(self):
        return "Queue length: " + str(self.get_length())

    def add_customer(self, q_id: int, customer: Customer):
        """
        Adds a customer to the queue.

        :param q_id: Queue ID to add customer to. Only used for sanity check.
        :param customer: Customer to add.
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

    def remove_customer(self, q_id: int):
        """
        Removes a customer from the queue.
        :return: Customer removed from queue.
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

        return self.queue.popleft()

    def get_length(self):
        """
        Returns the length of the queue.

        :return: Length of queue.
        """
        queue_length = len(self.queue)
        if queue_length < 0:
            raise ValueError("Queue length cannot be negative.")
        return queue_length
