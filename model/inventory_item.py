class InventoryItem:
    """
    An item that can be added to an inventory
    """

    _name: str

    def __init__(self, name: str):
        """
        Initializes the class

        :param name: The name of the item
        """
        self._name = name

    @property
    def name(self) -> str:
        return self._name
