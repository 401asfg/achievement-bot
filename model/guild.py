from model.inventory.inventory import Inventory
from model.person import Person


class Guild(Inventory[Person]):
    """
    A collection of people
    """
