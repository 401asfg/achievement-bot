from typing import Optional


class Achievement:
    """
    An achievement that a user can have
    """

    _name: str
    _description: Optional[str]

    def __init__(self, name, description=None):
        """
        Initializes the class

        :param name: The name of the achievement
        :param description: The description of the achievement
        """
        self._name = name
        self._description = description

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description
