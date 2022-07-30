from src.model.inventory.inventory import Inventory
from src.model.person import Person


class Guild(Inventory[Person]):
    """
    A collection of people
    """
