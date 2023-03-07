class CQueue:
    """We call it CQueue because Queue is already taken by the queue module."""

    def __init__(self):
        self.logstr = {"className": self.__class__.__name__}
        self.queue_len: int = 0

    def __str__(self):
        return "Queue length: " + str(self.queue_len)

    def get_length(self):
        """
        Returns current queue length.
        :return: Length of queue.
        """
        if self.queue_len < 0:
            raise ValueError("Queue length cannot be negative.")
        return self.queue_len

    def add_customer(self):
        """
        Adds a customer to the queue.
        """
        self.queue_len += 1
