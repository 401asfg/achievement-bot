import unittest

from model.inventory.inventory_item import InventoryItem


class TestInventoryItem(unittest.TestCase):
    NAME_A = "Name A"
    NAME_B = "Name B"
    NAME_C = "Name C"

    def test_init(self):
        def assert_init(name: str):
            inventory_item: InventoryItem
            inventory_item = InventoryItem(name)
            self.assertEqual(name, inventory_item.name)

        assert_init(self.NAME_A)
        assert_init(self.NAME_B)
        assert_init(self.NAME_C)


if __name__ == '__main__':
    unittest.main()
