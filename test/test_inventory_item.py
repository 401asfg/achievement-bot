import unittest
from typing import Optional

from model.inventory_item import InventoryItem


class TestInventoryItem(unittest.TestCase):
    name_a = "Name A"
    name_b = "Name B"
    name_c = "Name C"

    def test_init(self):
        def assert_init(name: str):
            inventory_item: InventoryItem
            inventory_item = InventoryItem(name)
            self.assertEqual(name, inventory_item.name)

        assert_init(self.name_a)
        assert_init(self.name_b)
        assert_init(self.name_c)


if __name__ == '__main__':
    unittest.main()
