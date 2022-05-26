import unittest
from typing import List

from model.achievement import Achievement
from model.guild import Guild
from model.guild_manager import GuildManager
from model.member import Member


class TestGuildManager(unittest.TestCase):
    guild: Guild
    guild_manager: GuildManager

    member_name_a = "Member A"
    member_name_b = "Member B"
    member_name_c = "Member C"

    achievement_name_a = "Achievement A"
    achievement_name_b = "Achievement B"
    achievement_name_c = "Achievement C"
    achievement_name_d = "Achievement D"
    achievement_name_e = "Achievement E"
    achievement_name_f = "Achievement F"

    achievement_a: Achievement
    achievement_b: Achievement
    achievement_c: Achievement
    achievement_d: Achievement
    achievement_e: Achievement
    achievement_f: Achievement

    def setUp(self) -> None:
        self.guild = Guild()
        self.guild_manager = GuildManager(self.guild)

        self.achievement_a = Achievement(self.achievement_name_a)
        self.achievement_b = Achievement(self.achievement_name_b)
        self.achievement_c = Achievement(self.achievement_name_c)
        self.achievement_d = Achievement(self.achievement_name_d)
        self.achievement_e = Achievement(self.achievement_name_e)
        self.achievement_f = Achievement(self.achievement_name_f)

    def test_init(self):
        self.assertEqual(0, self.guild_manager.guild_size())
        self.assertFalse(self.guild_manager.guild_contains(self.member_name_a))
        self.assertFalse(self.guild_manager.guild_contains(self.member_name_b))
        self.assertFalse(self.guild_manager.guild_contains(self.member_name_c))

    def test_query_guild(self):
        def assert_state(expected_size: int,
                         expected_contains_a: bool,
                         expected_contains_b: bool,
                         expected_contains_c: bool):
            self.assertEqual(expected_size, self.guild_manager.guild_size())
            self.assertEqual(expected_contains_a, self.guild_manager.guild_contains(self.member_name_a))
            self.assertEqual(expected_contains_b, self.guild_manager.guild_contains(self.member_name_b))
            self.assertEqual(expected_contains_c, self.guild_manager.guild_contains(self.member_name_c))

        def assert_fail(member: str,
                        members: List[str],
                        expected_size: int,
                        expected_contains_a: bool,
                        expected_contains_b: bool,
                        expected_contains_c: bool):
            try:
                self.guild_manager.query_guild(member, members)
                self.fail()
            except ValueError:
                pass

            assert_state(expected_size, expected_contains_a, expected_contains_b, expected_contains_c)

        def assert_member_not_in_members_fail(expected_size: int,
                                              expected_contains_a: bool,
                                              expected_contains_b: bool,
                                              expected_contains_c: bool):
            assert_fail(self.member_name_a,
                        [],
                        expected_size,
                        expected_contains_a,
                        expected_contains_b,
                        expected_contains_c)
            assert_fail(self.member_name_b,
                        [],
                        expected_size,
                        expected_contains_a,
                        expected_contains_b,
                        expected_contains_c)
            assert_fail(self.member_name_c,
                        [],
                        expected_size,
                        expected_contains_a,
                        expected_contains_b,
                        expected_contains_c)
            assert_fail(self.member_name_a,
                        [self.member_name_c],
                        expected_size,
                        expected_contains_a,
                        expected_contains_b,
                        expected_contains_c)
            assert_fail(self.member_name_b,
                        [self.member_name_a],
                        expected_size,
                        expected_contains_a,
                        expected_contains_b,
                        expected_contains_c)
            assert_fail(self.member_name_c,
                        [self.member_name_b],
                        expected_size,
                        expected_contains_a,
                        expected_contains_b,
                        expected_contains_c)
            assert_fail(self.member_name_a,
                        [self.member_name_b, self.member_name_c],
                        expected_size,
                        expected_contains_a,
                        expected_contains_b,
                        expected_contains_c)
            assert_fail(self.member_name_b,
                        [self.member_name_a, self.member_name_c],
                        expected_size,
                        expected_contains_a,
                        expected_contains_b,
                        expected_contains_c)
            assert_fail(self.member_name_c,
                        [self.member_name_a, self.member_name_b],
                        expected_size,
                        expected_contains_a,
                        expected_contains_b,
                        expected_contains_c)

        def assert_pass_and_member_not_in_members_fail(expected_member_size: int,
                                                       expected_size: int,
                                                       expected_contains_a: bool,
                                                       expected_contains_b: bool,
                                                       expected_contains_c: bool,
                                                       member: str,
                                                       members: List[str]) -> Member:
            actual_member = self.guild_manager.query_guild(member, members)
            self.assertEqual(member, actual_member.name)
            self.assertEqual(expected_member_size, actual_member.size())
            assert_state(expected_size, expected_contains_a, expected_contains_b, expected_contains_c)
            assert_member_not_in_members_fail(expected_size,
                                              expected_contains_a,
                                              expected_contains_b,
                                              expected_contains_c)
            return actual_member

        assert_member_not_in_members_fail(0, False, False, False)
        assert_pass_and_member_not_in_members_fail(0,
                                                   1,
                                                   True,
                                                   False,
                                                   False,
                                                   self.member_name_a,
                                                   [self.member_name_a])

        assert_pass_and_member_not_in_members_fail(0,
                                                   1,
                                                   True,
                                                   False,
                                                   False,
                                                   self.member_name_a,
                                                   [self.member_name_a, self.member_name_b, self.member_name_c])

        member_b = assert_pass_and_member_not_in_members_fail(0,
                                                              2,
                                                              True,
                                                              True,
                                                              False,
                                                              self.member_name_b,
                                                              [self.member_name_a, self.member_name_b,
                                                               self.member_name_c])

        member_b.add(self.achievement_a)
        member_b.add(self.achievement_b)
        member_b.add(self.achievement_c)
        member_b.add(self.achievement_d)

        assert_pass_and_member_not_in_members_fail(4,
                                                   2,
                                                   True,
                                                   True,
                                                   False,
                                                   self.member_name_b,
                                                   [self.member_name_b])

        assert_pass_and_member_not_in_members_fail(0,
                                                   2,
                                                   True,
                                                   True,
                                                   False,
                                                   self.member_name_a,
                                                   [self.member_name_a, self.member_name_c])

        member_c = assert_pass_and_member_not_in_members_fail(0,
                                                              3,
                                                              True,
                                                              True,
                                                              True,
                                                              self.member_name_c,
                                                              [self.member_name_b, self.member_name_c])

        member_c.add(self.achievement_e)
        member_c.add(self.achievement_f)

        assert_pass_and_member_not_in_members_fail(2,
                                                   3,
                                                   True,
                                                   True,
                                                   True,
                                                   self.member_name_c,
                                                   [self.member_name_c])

        assert_pass_and_member_not_in_members_fail(4,
                                                   3,
                                                   True,
                                                   True,
                                                   True,
                                                   self.member_name_b,
                                                   [self.member_name_c, self.member_name_b])

    # TODO: write rest of tests


if __name__ == '__main__':
    unittest.main()
