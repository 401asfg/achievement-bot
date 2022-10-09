from datetime import date
from typing import Optional

from src.content.error_messages import ACHIEVEMENT_IS_NAMELESS_ERROR_MSG
from src.model.inventory.inventory_item import InventoryItem


class Achievement(InventoryItem):
    """
    An achievement that a person can have
    """

    BESTOWER_JSON_KEY = "bestower"
    DATE_ACHIEVED_JSON_KEY = "date achieved"

    _bestower: str
    _date_achieved: date

    def __init__(self, name: str, bestower: str, date_achieved: date):
        """
        Initializes the class

        :param name: The name of the item
        :param bestower: The name of the bestower of this achievement
        :param date_achieved: The date on which this achievement was achieved
        :raise ValueError: If the given name is blank
        """

        if not name or name.isspace():
            raise ValueError(ACHIEVEMENT_IS_NAMELESS_ERROR_MSG )

        super().__init__(name)
        self._bestower = bestower
        self._date_achieved = date_achieved

    @property
    def bestower(self) -> str:
        return self._bestower

    @property
    def date_achieved(self) -> date:
        return self._date_achieved

    def to_json(self) -> Optional[dict]:
        json = super().to_json()
        json[self.BESTOWER_JSON_KEY] = self._bestower
        json[self.DATE_ACHIEVED_JSON_KEY] = str(self._date_achieved)
        return json
