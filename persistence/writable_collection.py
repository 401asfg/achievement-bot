from abc import ABC, abstractmethod
from typing import Optional, List

from persistence.writable import Writable


class WritableCollection(Writable):
    """
    Can be converted to a JSON like object that holds an array of JSON like objects
    """

    @abstractmethod
    def array_to_json(self) -> List[dict]:
        """
        :return: The data of the class represented as a JSON like object that holds an array of JSON like objects
        """
        return []
