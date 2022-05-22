from model.achievement import Achievement
from model.inventory import Inventory

from model.inventory_item import InventoryItem

# TODO: test


class Member(InventoryItem, Inventory[Achievement]):
    """
    A member of the guild that can hold achievements
    """
