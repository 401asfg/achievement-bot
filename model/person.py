from typing import List

from model.achievement import Achievement
from model.inventory.inventory import Inventory

from model.inventory.inventory_item import InventoryItem


class Person(InventoryItem, Inventory[Achievement]):
    """
    A member of the community that can hold achievements
    """

    def __init__(self, name: str):
        super().__init__(name)
        self._items = {}            # TODO: discover a way to inherit this from Inventory

    def get_achievements(self) -> List[Achievement]:
        """
        :return: All of the achievements that the person has
        """
        return list(self._items.values())
