from typing import List, Optional

from src.model.achievement import Achievement
from src.model.inventory.inventory import Inventory

from src.model.inventory.inventory_item import InventoryItem


class Person(InventoryItem, Inventory[Achievement]):
    """
    A member of the community that can hold achievements
    """

    def __init__(self, name: str):
        """
        Initializes the class

        :param name: The name of the person
        """
        super().__init__(name)
        self._items = {}            # TODO: discover a way to inherit this from Inventory

    def get_achievements(self) -> List[Achievement]:
        """
        :return: All of the achievements that the person has
        """
        return list(self._items.values())

    def to_json(self) -> Optional[dict]:
        json = super().to_json()
        json[self.ITEMS_JSON_KEY] = super().array_to_json()
        return json
