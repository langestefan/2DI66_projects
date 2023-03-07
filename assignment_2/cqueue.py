class CQueue:
    """We call it CQueue because Queue is already taken by the queue module."""

    def __init__(self):
        self.queue_len = 0

    def __str__(self):
        return "Queue length: " + str(self.queue_len)

    def get_queue_length(self):
        """
        Returns current queue length.
        :return: Length of queue.
        """
        return self.queue_len
