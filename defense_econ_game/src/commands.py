class Command:
    """
    Represents a command to be executed in the game.

    Attributes:
        type (str): The type of the command.
        payload (any, optional): The payload of the command. Defaults to None.
    """
    def __init__(self, type, payload=None):
        """
        Initializes the Command.

        Args:
            type (str): The type of the command.
            payload (any, optional): The payload of the command. Defaults to None.
        """
        self.type = type
        self.payload = payload
