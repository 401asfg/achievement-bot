import unittest

from src.model.inventory.inventory_item import InventoryItem


class TestInventoryItem(unittest.TestCase):
    NAME_A = "Name A"
    NAME_B = "Name B"
    NAME_C = "Name C"

    inventory_item_a: InventoryItem
    inventory_item_b: InventoryItem
    inventory_item_c: InventoryItem

    def setUp(self) -> None:
        self.inventory_item_a = InventoryItem(self.NAME_A)
        self.inventory_item_b = InventoryItem(self.NAME_B)
        self.inventory_item_c = InventoryItem(self.NAME_C)

    def test_init(self):
        def assert_init(inventory_item: InventoryItem, expected_name: str):
            self.assertEqual(expected_name, inventory_item.name)

        assert_init(self.inventory_item_a, self.NAME_A)
        assert_init(self.inventory_item_b, self.NAME_B)
        assert_init(self.inventory_item_c, self.NAME_C)

    def test_to_json(self):
        def assert_to_json(expected_json: dict, inventory_item: InventoryItem):
            actual_json = inventory_item.to_json()
            self.assertEqual(expected_json, actual_json)

        assert_to_json({InventoryItem.NAME_JSON_KEY: self.NAME_A}, self.inventory_item_a)
        assert_to_json({InventoryItem.NAME_JSON_KEY: self.NAME_B}, self.inventory_item_b)
        assert_to_json({InventoryItem.NAME_JSON_KEY: self.NAME_C}, self.inventory_item_c)


if __name__ == '__main__':
    unittest.main()
