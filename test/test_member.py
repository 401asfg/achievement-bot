import unittest

from model.achievement import Achievement
from model.inventory.exceptions.inventory_contains_item_error import InventoryContainsItemError
from model.inventory.exceptions.inventory_item_not_found_error import InventoryItemNotFoundError
from model.member import Member


class TestMember(unittest.TestCase):
    member_name = "Member"

    member: Member

    name_a = "Achievement A"
    name_b = "Achievement B"
    name_c = "Achievement C"
    name_d = "Achievement D"

    achievement_a: Achievement
    achievement_b: Achievement
    achievement_c: Achievement
    achievement_d: Achievement

    def setUp(self) -> None:
        self.member = Member(self.member_name)

        self.achievement_a = Achievement(self.name_a)
        self.achievement_b = Achievement(self.name_b)
        self.achievement_c = Achievement(self.name_c)
        self.achievement_d = Achievement(self.name_d)

    def test_init(self):
        self.assertEqual(self.member_name, self.member.name)
        self.assertEqual(0, self.member.size())
        self.assertFalse(self.member.contains(self.name_a))
        self.assertFalse(self.member.contains(self.name_b))
        self.assertFalse(self.member.contains(self.name_c))
        self.assertFalse(self.member.contains(self.name_d))

    def test_get_achievement_names(self):
        self.member.add(self.achievement_a)
        self.member.add(self.achievement_b)
        self.member.add(self.achievement_c)
        self.assertEqual([self.name_a, self.name_b, self.name_c], self.member.get_achievement_names())

    def test_add(self):
        def assert_state(size: int, contains_a: bool, contains_b: bool, contains_c: bool, contains_d: bool):
            self.assertEqual(size, self.member.size())
            self.assertEqual(contains_a, self.member.contains(self.name_a))
            self.assertEqual(contains_b, self.member.contains(self.name_b))
            self.assertEqual(contains_c, self.member.contains(self.name_c))
            self.assertEqual(contains_d, self.member.contains(self.name_d))

        def assert_pass(achievement: Achievement,
                        size: int,
                        contains_a: bool,
                        contains_b: bool,
                        contains_c: bool,
                        contains_d: bool):
            self.member.add(achievement)
            assert_state(size, contains_a, contains_b, contains_c, contains_d)

        def assert_fail(achievement: Achievement,
                        size: int,
                        contains_a: bool,
                        contains_b: bool,
                        contains_c: bool,
                        contains_d: bool):
            try:
                self.member.add(achievement)
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

    def test_get(self):
        def assert_pass(achievement_name: str, expected_achievement: Achievement):
            actual_achievement = self.member.get(achievement_name)
            self.assertEqual(expected_achievement, actual_achievement)

        def assert_fail(achievement_name: str):
            try:
                self.member.get(achievement_name)
                self.fail()
            except InventoryItemNotFoundError:
                pass

        assert_fail(self.name_a)
        assert_fail(self.name_b)
        assert_fail(self.name_c)
        assert_fail(self.name_d)

        self.member.add(self.achievement_b)
        assert_fail(self.name_a)
        assert_pass(self.name_b, self.achievement_b)
        assert_fail(self.name_c)
        assert_fail(self.name_d)

        self.member.add(self.achievement_d)
        assert_fail(self.name_a)
        assert_pass(self.name_b, self.achievement_b)
        assert_fail(self.name_c)
        assert_pass(self.name_d, self.achievement_d)

        self.member.add(self.achievement_a)
        assert_pass(self.name_a, self.achievement_a)
        assert_pass(self.name_b, self.achievement_b)
        assert_fail(self.name_c)
        assert_pass(self.name_d, self.achievement_d)

        self.member.add(self.achievement_c)
        assert_pass(self.name_a, self.achievement_a)
        assert_pass(self.name_b, self.achievement_b)
        assert_pass(self.name_c, self.achievement_c)
        assert_pass(self.name_d, self.achievement_d)


if __name__ == '__main__':
    unittest.main()
