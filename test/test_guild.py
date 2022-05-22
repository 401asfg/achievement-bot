import unittest

from model.inventory.exceptions.inventory_contains_item_error import InventoryContainsItemError
from model.inventory.exceptions.inventory_item_not_found_error import InventoryItemNotFoundError

from model.guild import Guild
from model.member import Member


class TestGuild(unittest.TestCase):
    guild: Guild

    name_a = "Member A"
    name_b = "Member B"
    name_c = "Member C"
    name_d = "Member D"

    member_a: Member
    member_b: Member
    member_c: Member
    member_d: Member

    def setUp(self) -> None:
        self.guild = Guild()

        self.member_a = Member(self.name_a)
        self.member_b = Member(self.name_b)
        self.member_c = Member(self.name_c)
        self.member_d = Member(self.name_d)

    def test_init(self):
        self.assertEqual(0, self.guild.size())
        self.assertFalse(self.guild.contains(self.name_a))
        self.assertFalse(self.guild.contains(self.name_b))
        self.assertFalse(self.guild.contains(self.name_c))
        self.assertFalse(self.guild.contains(self.name_d))

    def test_add(self):
        def assert_state(size: int, contains_a: bool, contains_b: bool, contains_c: bool, contains_d: bool):
            self.assertEqual(size, self.guild.size())
            self.assertEqual(contains_a, self.guild.contains(self.name_a))
            self.assertEqual(contains_b, self.guild.contains(self.name_b))
            self.assertEqual(contains_c, self.guild.contains(self.name_c))
            self.assertEqual(contains_d, self.guild.contains(self.name_d))

        def assert_pass(member: Member,
                        size: int,
                        contains_a: bool,
                        contains_b: bool,
                        contains_c: bool,
                        contains_d: bool):
            self.guild.add(member)
            assert_state(size, contains_a, contains_b, contains_c, contains_d)

        def assert_fail(member: Member,
                        size: int,
                        contains_a: bool,
                        contains_b: bool,
                        contains_c: bool,
                        contains_d: bool):
            try:
                self.guild.add(member)
                self.fail()
            except InventoryContainsItemError:
                pass

            assert_state(size, contains_a, contains_b, contains_c, contains_d)

        def assert_pass_and_fail(member: Member,
                                 size: int,
                                 contains_a: bool,
                                 contains_b: bool,
                                 contains_c: bool,
                                 contains_d: bool):
            assert_pass(member, size, contains_a, contains_b, contains_c, contains_d)
            assert_fail(member, size, contains_a, contains_b, contains_c, contains_d)

        assert_state(0, False, False, False, False)

        assert_pass_and_fail(self.member_a, 1, True, False, False, False)

        assert_pass_and_fail(self.member_c, 2, True, False, True, False)

        assert_fail(self.member_a, 2, True, False, True, False)

        assert_pass_and_fail(self.member_b, 3, True, True, True, False)

        assert_fail(self.member_a, 3, True, True, True, False)
        assert_fail(self.member_b, 3, True, True, True, False)
        assert_fail(self.member_c, 3, True, True, True, False)

        assert_pass_and_fail(self.member_d, 4, True, True, True, True)

        assert_fail(self.member_a, 4, True, True, True, True)
        assert_fail(self.member_b, 4, True, True, True, True)
        assert_fail(self.member_c, 4, True, True, True, True)
        assert_fail(self.member_d, 4, True, True, True, True)

    def test_get(self):
        def assert_pass(member_name: str, expected_member: Member):
            actual_member = self.guild.get(member_name)
            self.assertEqual(expected_member, actual_member )

        def assert_fail(member_name: str):
            try:
                self.guild.get(member_name)
                self.fail()
            except InventoryItemNotFoundError:
                pass

        assert_fail(self.name_a)
        assert_fail(self.name_b)
        assert_fail(self.name_c)
        assert_fail(self.name_d)

        self.guild.add(self.member_b)
        assert_fail(self.name_a)
        assert_pass(self.name_b, self.member_b)
        assert_fail(self.name_c)
        assert_fail(self.name_d)

        self.guild.add(self.member_d)
        assert_fail(self.name_a)
        assert_pass(self.name_b, self.member_b)
        assert_fail(self.name_c)
        assert_pass(self.name_d, self.member_d)

        self.guild.add(self.member_a)
        assert_pass(self.name_a, self.member_a)
        assert_pass(self.name_b, self.member_b)
        assert_fail(self.name_c)
        assert_pass(self.name_d, self.member_d)

        self.guild.add(self.member_c)
        assert_pass(self.name_a, self.member_a)
        assert_pass(self.name_b, self.member_b)
        assert_pass(self.name_c, self.member_c)
        assert_pass(self.name_d, self.member_d)


if __name__ == '__main__':
    unittest.main()
