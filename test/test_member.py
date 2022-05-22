import unittest

from model.achievement import Achievement
from model.member import Member


class TestMember(unittest.TestCase):
    member: Member

    name_a = "Achievement A"
    name_b = "Achievement B"
    name_c = "Achievement C"

    achievement_a: Achievement
    achievement_b: Achievement
    achievement_c: Achievement

    def setUp(self) -> None:
        self.member = Member("")
        self.achievement_a = Achievement(self.name_a)
        self.achievement_b = Achievement(self.name_b)
        self.achievement_c = Achievement(self.name_c)

    def test_get_achievement_names(self):
        self.member.add(self.achievement_a)
        self.member.add(self.achievement_b)
        self.member.add(self.achievement_c)
        self.assertEqual([self.name_a, self.name_b, self.name_c], self.member.get_achievement_names())


if __name__ == '__main__':
    unittest.main()
