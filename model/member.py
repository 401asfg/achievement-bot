from typing import List

from model.achievement import Achievement
from model.inventory.inventory import Inventory

from model.inventory.inventory_item import InventoryItem


class Member(InventoryItem, Inventory[Achievement]):
    """
    A member of the guild that can hold achievements
    """

    def __init__(self, name: str):
        super().__init__(name)
        self._items = {}            # TODO: discover a way to inherit this from Inventory

    def get_achievement_names(self) -> List[str]:
        """
        :return: The names of all the achievements that the member has
        """
        return list(self._items.keys())
