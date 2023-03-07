class Server:
    """Server class"""

    def __init__(self, id: int):
        self.id = id

    def __str__(self):
        return "Server id: " + str(self.id)

    def get_id(self):
        return self.id
