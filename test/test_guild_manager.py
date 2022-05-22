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

    member_a: Member
    member_b: Member
    member_c: Member

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

        self.member_a = Member(self.member_name_a)
        self.member_b = Member(self.member_name_b)
        self.member_c = Member(self.member_name_c)

        self.achievement_a = Achievement(self.achievement_name_a)
        self.achievement_b = Achievement(self.achievement_name_b)
        self.achievement_c = Achievement(self.achievement_name_c)
        self.achievement_d = Achievement(self.achievement_name_d)
        self.achievement_e = Achievement(self.achievement_name_e)
        self.achievement_f = Achievement(self.achievement_name_f)

    def test_query_guild(self):
        def assert_fail(member: str, members: List[str]):
            try:
                self.guild_manager.query_guild(member, members)
                self.fail()
            except ValueError:
                pass

        def assert_pass(expected_member: Member, member: str, members: List[str]):
            actual_member = self.guild_manager.query_guild(member, members)
            self.assertEqual(expected_member, actual_member)

        assert_fail(self.member_name_a, [])
        assert_fail(self.member_name_b, [])
        assert_fail(self.member_name_c, [])
        assert_fail(self.member_name_a, [self.member_name_b, self.member_c])
        assert_fail(self.member_name_b, [self.member_name_a, self.member_c])
        assert_fail(self.member_name_c, [self.member_name_a, self.member_b])

        # TODO: write rest of this test

    # TODO: write other tests


if __name__ == '__main__':
    unittest.main()
