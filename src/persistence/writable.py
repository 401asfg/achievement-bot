from abc import ABC, abstractmethod
from typing import Optional


class Writable(ABC):
    """
    Can be converted to a JSON like object
    """

    @abstractmethod
    def to_json(self) -> Optional[dict]:
        """
        :return: The data of the class represented as a JSON like object
        """
        return None
