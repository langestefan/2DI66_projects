class Server:
    """Server class"""

    def __init__(self, id: int):
        self.server_id = id

    def __str__(self):
        return "Server id: " + str(self.get_id())

    def get_id(self):
        """
        Returns the ID of the server.
        """
        return self.server_id
