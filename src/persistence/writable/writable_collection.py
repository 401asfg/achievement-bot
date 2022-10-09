from abc import abstractmethod
from typing import List

from src.persistence.writable.writable import Writable


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
