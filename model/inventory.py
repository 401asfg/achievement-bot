from typing import Dict, TypeVar, Generic

from model.inventory_exceptions.inventory_contains_item_error import InventoryContainsItemError
from model.inventory_exceptions.inventory_item_not_found_error import InventoryItemNotFoundError
from model.inventory_item import InventoryItem

T = TypeVar("T", bound=InventoryItem)

# TODO: test


class Inventory(Generic[T]):
    """
    An inventory that can hold inventory items
    """

    _items: Dict[str, T]
    _index: int

    def __init__(self):
        """
        Initializes the class
        """
        self._items = {}

    def size(self) -> int:
        """
        :return: The number of items in this inventory
        """
        return len(self._items)

    def contains(self, item_name: str) -> bool:
        """
        :param item_name: The name of the item to check this inventory for
        :return: True if this inventory contains an item with given name; otherwise, False
        """
        return item_name in self._items

    def get(self, item_name: str) -> T:
        """
        :param item_name: The name of the item to get
        :return: The item of the given name
        :raise InventoryItemNotFoundError: If the given item_name corresponds to no item in this inventory
        """

        if not self.contains(item_name):
            raise InventoryItemNotFoundError(f"The inventory doesn't have the {item_name} item")

        return self._items[item_name]

    def add(self, item: T):
        """
        Adds an item to this inventory

        :param item: The item to add
        :raise InventoryContainsItemError: If the item was already added to the inventory
        """

        if self.contains(item.name):
            raise InventoryContainsItemError(f"The inventory already has the {item.name} item")

        self._items[item.name] = item

    def __iter__(self):
        """
        Set the iteration index to 0

        :return: This inventory
        """
        self._index = 0
        return self

    def __next__(self):
        """
        :return: The next item
        :raise StopIteration: If there is no next item
        """

        if self._index >= self.size():
            raise StopIteration

        values = list(self._items.values())
        result = values[self._index]
        self._index += 1
        return result
