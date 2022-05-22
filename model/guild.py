from model.inventory.inventory import Inventory
from model.member import Member


class Guild(Inventory[Member]):
    """
    A guild that can hold members
    """
