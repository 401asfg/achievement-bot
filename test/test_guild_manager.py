import unittest

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
        self.achievement_a = Achievement(self.achievement_name_a)
        self.achievement_b = Achievement(self.achievement_name_b)
        self.achievement_c = Achievement(self.achievement_name_c)
        self.achievement_d = Achievement(self.achievement_name_d)
        self.achievement_e = Achievement(self.achievement_name_e)
        self.achievement_f = Achievement(self.achievement_name_f)

        self.member_a = Member(self.member_name_a)
        self.member_a.add(self.achievement_a)
        self.member_a.add(self.achievement_b)

        self.member_b = Member(self.member_name_b)
        self.member_b.add(self.achievement_c)
        self.member_b.add(self.achievement_d)

        self.member_c = Member(self.member_name_c)
        self.member_c.add(self.achievement_e)
        self.member_c.add(self.achievement_f)

        self.guild = Guild()
        self.guild.add(self.member_a)
        self.guild.add(self.member_b)
        self.guild.add(self.member_c)


if __name__ == '__main__':
    unittest.main()
