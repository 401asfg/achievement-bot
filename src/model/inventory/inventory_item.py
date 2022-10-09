from typing import Optional

from src.persistence.writable.writable import Writable


class InventoryItem(Writable):
    """
    An item that can be added to an inventory
    """

    NAME_JSON_KEY = "name"

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

    def to_json(self) -> Optional[dict]:
        return {
            self.NAME_JSON_KEY: self._name
        }
