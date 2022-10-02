from typing import Optional

from src.content.error_messages import ACHIEVEMENT_IS_NAMELESS_ERROR_MSG
from src.model.inventory.inventory_item import InventoryItem

# TODO: add description property


class Achievement(InventoryItem):
    """
    An achievement that a person can have
    """

    BESTOWER_JSON_KEY = "bestower"

    _bestower: str

    def __init__(self, name: str, bestower: str):
        """
        Initializes the class

        :param name: The name of the item
        :param bestower: The name of the bestower of this achievement
        :raise ValueError: If the given name is blank
        """
        if not name or name.isspace():
            raise ValueError(ACHIEVEMENT_IS_NAMELESS_ERROR_MSG )

        super().__init__(name)
        self._bestower = bestower

    @property
    def bestower(self) -> str:
        return self._bestower

    def to_json(self) -> Optional[dict]:
        json = super().to_json()
        json[self.BESTOWER_JSON_KEY] = self._bestower
        return json
