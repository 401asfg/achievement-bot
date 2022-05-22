import unittest

from model.inventory.exceptions.inventory_contains_item_error import InventoryContainsItemError
from model.inventory.exceptions.inventory_item_not_found_error import InventoryItemNotFoundError
from model.inventory.inventory import Inventory
from model.inventory.inventory_item import InventoryItem


class TestInventory(unittest.TestCase):
    inventory: Inventory

    name_a = "Item A"
    name_b = "Item B"
    name_c = "Item C"
    name_d = "Item D"

    item_a: InventoryItem
    item_b: InventoryItem
    item_c: InventoryItem
    item_d: InventoryItem

    def setUp(self) -> None:
        self.inventory = Inventory()

        self.item_a = InventoryItem(self.name_a)
        self.item_b = InventoryItem(self.name_b)
        self.item_c = InventoryItem(self.name_c)
        self.item_d = InventoryItem(self.name_d)

    def test_init(self):
        self.assertEqual(0, self.inventory.size())
        self.assertFalse(self.inventory.contains(self.name_a))
        self.assertFalse(self.inventory.contains(self.name_b))
        self.assertFalse(self.inventory.contains(self.name_c))
        self.assertFalse(self.inventory.contains(self.name_d))

    def test_add(self):
        def assert_state(size: int, contains_a: bool, contains_b: bool, contains_c: bool, contains_d: bool):
            self.assertEqual(size, self.inventory.size())
            self.assertEqual(contains_a, self.inventory.contains(self.name_a))
            self.assertEqual(contains_b, self.inventory.contains(self.name_b))
            self.assertEqual(contains_c, self.inventory.contains(self.name_c))
            self.assertEqual(contains_d, self.inventory.contains(self.name_d))

        def assert_pass(item: InventoryItem,
                        size: int,
                        contains_a: bool,
                        contains_b: bool,
                        contains_c: bool,
                        contains_d: bool):
            self.inventory.add(item)
            assert_state(size, contains_a, contains_b, contains_c, contains_d)

        def assert_fail(item: InventoryItem,
                        size: int,
                        contains_a: bool,
                        contains_b: bool,
                        contains_c: bool,
                        contains_d: bool):
            try:
                self.inventory.add(item)
                self.fail()
            except InventoryContainsItemError:
                pass

            assert_state(size, contains_a, contains_b, contains_c, contains_d)

        def assert_pass_and_fail(item: InventoryItem,
                                 size: int,
                                 contains_a: bool,
                                 contains_b: bool,
                                 contains_c: bool,
                                 contains_d: bool):
            assert_pass(item, size, contains_a, contains_b, contains_c, contains_d)
            assert_fail(item, size, contains_a, contains_b, contains_c, contains_d)

        assert_state(0, False, False, False, False)

        assert_pass_and_fail(self.item_a, 1, True, False, False, False)

        assert_pass_and_fail(self.item_c, 2, True, False, True, False)

        assert_fail(self.item_a, 2, True, False, True, False)

        assert_pass_and_fail(self.item_b, 3, True, True, True, False)

        assert_fail(self.item_a, 3, True, True, True, False)
        assert_fail(self.item_b, 3, True, True, True, False)
        assert_fail(self.item_c, 3, True, True, True, False)

        assert_pass_and_fail(self.item_d, 4, True, True, True, True)

        assert_fail(self.item_a, 4, True, True, True, True)
        assert_fail(self.item_b, 4, True, True, True, True)
        assert_fail(self.item_c, 4, True, True, True, True)
        assert_fail(self.item_d, 4, True, True, True, True)

    def test_get(self):
        def assert_pass(item_name: str, expected_item: InventoryItem):
            actual_item = self.inventory.get(item_name)
            self.assertEqual(expected_item, actual_item)

        def assert_fail(item_name: str):
            try:
                self.inventory.get(item_name)
                self.fail()
            except InventoryItemNotFoundError:
                pass

        assert_fail(self.name_a)
        assert_fail(self.name_b)
        assert_fail(self.name_c)
        assert_fail(self.name_d)

        self.inventory.add(self.item_b)
        assert_fail(self.name_a)
        assert_pass(self.name_b, self.item_b)
        assert_fail(self.name_c)
        assert_fail(self.name_d)

        self.inventory.add(self.item_d)
        assert_fail(self.name_a)
        assert_pass(self.name_b, self.item_b)
        assert_fail(self.name_c)
        assert_pass(self.name_d, self.item_d)

        self.inventory.add(self.item_a)
        assert_pass(self.name_a, self.item_a)
        assert_pass(self.name_b, self.item_b)
        assert_fail(self.name_c)
        assert_pass(self.name_d, self.item_d)

        self.inventory.add(self.item_c)
        assert_pass(self.name_a, self.item_a)
        assert_pass(self.name_b, self.item_b)
        assert_pass(self.name_c, self.item_c)
        assert_pass(self.name_d, self.item_d)


if __name__ == '__main__':
    unittest.main()
