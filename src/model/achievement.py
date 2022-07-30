from typing import Optional

from src.model.inventory.inventory_item import InventoryItem

# TODO: add description property


class Achievement(InventoryItem):
    """
    An achievement that a person can have
    """
    _bestower: str

    def __init__(self, name: str, bestower: str):
        """
        Initializes the class

        :param name: The name of the item
        :param bestower: The name of the bestower of this achievement
        """
        super().__init__(name)
        self._bestower = bestower

    @property
    def bestower(self) -> str:
        return self._bestower

    def to_json(self) -> Optional[dict]:
        json = super().to_json()
        json["bestower"] = self._bestower
        return json
