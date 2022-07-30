import unittest
from typing import List

from src.model.achievement import Achievement
from src.model.inventory.exceptions.inventory_contains_item_error import InventoryContainsItemError
from src.model.inventory.exceptions.inventory_item_not_found_error import InventoryItemNotFoundError
from src.model.person import Person


class TestPerson(unittest.TestCase):
    PERSON_NAME = "Person"

    person: Person

    ACHIEVEMENT_NAME_A = "Achievement A"
    ACHIEVEMENT_NAME_B = "Achievement B"
    ACHIEVEMENT_NAME_C = "Achievement C"
    ACHIEVEMENT_NAME_D = "Achievement D"

    BESTOWER_A = "Bestower A"
    BESTOWER_B = "Bestower B"
    BESTOWER_C = "Bestower C"
    BESTOWER_D = "Bestower D"

    achievement_a: Achievement
    achievement_b: Achievement
    achievement_c: Achievement
    achievement_d: Achievement

    def setUp(self) -> None:
        self.person = Person(self.PERSON_NAME)

        self.achievement_a = Achievement(self.ACHIEVEMENT_NAME_A, self.BESTOWER_A)
        self.achievement_b = Achievement(self.ACHIEVEMENT_NAME_B, self.BESTOWER_B)
        self.achievement_c = Achievement(self.ACHIEVEMENT_NAME_C, self.BESTOWER_C)
        self.achievement_d = Achievement(self.ACHIEVEMENT_NAME_D, self.BESTOWER_D)

    def test_init(self):
        self.assertEqual(self.PERSON_NAME, self.person.name)
        self.assertEqual(0, self.person.size())
        self.assertFalse(self.person.contains(self.ACHIEVEMENT_NAME_A))
        self.assertFalse(self.person.contains(self.ACHIEVEMENT_NAME_B))
        self.assertFalse(self.person.contains(self.ACHIEVEMENT_NAME_C))
        self.assertFalse(self.person.contains(self.ACHIEVEMENT_NAME_D))

    def test_add(self):
        def assert_state(size: int, contains_a: bool, contains_b: bool, contains_c: bool, contains_d: bool):
            self.assertEqual(size, self.person.size())
            self.assertEqual(contains_a, self.person.contains(self.ACHIEVEMENT_NAME_A))
            self.assertEqual(contains_b, self.person.contains(self.ACHIEVEMENT_NAME_B))
            self.assertEqual(contains_c, self.person.contains(self.ACHIEVEMENT_NAME_C))
            self.assertEqual(contains_d, self.person.contains(self.ACHIEVEMENT_NAME_D))

        def assert_pass(achievement: Achievement,
                        size: int,
                        contains_a: bool,
                        contains_b: bool,
                        contains_c: bool,
                        contains_d: bool):
            self.person.add(achievement)
            assert_state(size, contains_a, contains_b, contains_c, contains_d)

        def assert_fail(achievement: Achievement,
                        size: int,
                        contains_a: bool,
                        contains_b: bool,
                        contains_c: bool,
                        contains_d: bool):
            try:
                self.person.add(achievement)
                self.fail()
            except InventoryContainsItemError:
                pass

            assert_state(size, contains_a, contains_b, contains_c, contains_d)

        def assert_pass_and_fail(achievement: Achievement,
                                 size: int,
                                 contains_a: bool,
                                 contains_b: bool,
                                 contains_c: bool,
                                 contains_d: bool):
            assert_pass(achievement, size, contains_a, contains_b, contains_c, contains_d)
            assert_fail(achievement, size, contains_a, contains_b, contains_c, contains_d)

        assert_state(0, False, False, False, False)

        assert_pass_and_fail(self.achievement_a, 1, True, False, False, False)

        assert_pass_and_fail(self.achievement_c, 2, True, False, True, False)

        assert_fail(self.achievement_a, 2, True, False, True, False)

        assert_pass_and_fail(self.achievement_b, 3, True, True, True, False)

        assert_fail(self.achievement_a, 3, True, True, True, False)
        assert_fail(self.achievement_b, 3, True, True, True, False)
        assert_fail(self.achievement_c, 3, True, True, True, False)

        assert_pass_and_fail(self.achievement_d, 4, True, True, True, True)

        assert_fail(self.achievement_a, 4, True, True, True, True)
        assert_fail(self.achievement_b, 4, True, True, True, True)
        assert_fail(self.achievement_c, 4, True, True, True, True)
        assert_fail(self.achievement_d, 4, True, True, True, True)

    def test_get_achievements(self):
        def assert_get_achievements(expected_achievements: List[Achievement]):
            self.assertEqual(expected_achievements, self.person.get_achievements())

        assert_get_achievements([])

        self.person.add(self.achievement_a)
        assert_get_achievements([self.achievement_a])

        self.person.add(self.achievement_b)
        assert_get_achievements([self.achievement_a, self.achievement_b])

        self.person.add(self.achievement_c)
        assert_get_achievements([self.achievement_a, self.achievement_b, self.achievement_c])

    def test_get(self):
        def assert_pass(achievement_name: str, expected_achievement: Achievement):
            actual_achievement = self.person.get(achievement_name)
            self.assertEqual(expected_achievement, actual_achievement)

        def assert_fail(achievement_name: str):
            try:
                self.person.get(achievement_name)
                self.fail()
            except InventoryItemNotFoundError:
                pass

        assert_fail(self.ACHIEVEMENT_NAME_A)
        assert_fail(self.ACHIEVEMENT_NAME_B)
        assert_fail(self.ACHIEVEMENT_NAME_C)
        assert_fail(self.ACHIEVEMENT_NAME_D)

        self.person.add(self.achievement_b)
        assert_fail(self.ACHIEVEMENT_NAME_A)
        assert_pass(self.ACHIEVEMENT_NAME_B, self.achievement_b)
        assert_fail(self.ACHIEVEMENT_NAME_C)
        assert_fail(self.ACHIEVEMENT_NAME_D)

        self.person.add(self.achievement_d)
        assert_fail(self.ACHIEVEMENT_NAME_A)
        assert_pass(self.ACHIEVEMENT_NAME_B, self.achievement_b)
        assert_fail(self.ACHIEVEMENT_NAME_C)
        assert_pass(self.ACHIEVEMENT_NAME_D, self.achievement_d)

        self.person.add(self.achievement_a)
        assert_pass(self.ACHIEVEMENT_NAME_A, self.achievement_a)
        assert_pass(self.ACHIEVEMENT_NAME_B, self.achievement_b)
        assert_fail(self.ACHIEVEMENT_NAME_C)
        assert_pass(self.ACHIEVEMENT_NAME_D, self.achievement_d)

        self.person.add(self.achievement_c)
        assert_pass(self.ACHIEVEMENT_NAME_A, self.achievement_a)
        assert_pass(self.ACHIEVEMENT_NAME_B, self.achievement_b)
        assert_pass(self.ACHIEVEMENT_NAME_C, self.achievement_c)
        assert_pass(self.ACHIEVEMENT_NAME_D, self.achievement_d)


if __name__ == '__main__':
    unittest.main()
