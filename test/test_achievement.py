import unittest
from typing import Optional

from model.achievement import Achievement


class TestAchievement(unittest.TestCase):
    name_a = "Name A"
    name_b = "Name B"
    name_c = "Name C"

    def test_init(self):
        def assert_init(name: str):
            achievement: Achievement
            achievement = Achievement(name)
            self.assertEqual(name, achievement.name)

        assert_init(self.name_a)
        assert_init(self.name_b)
        assert_init(self.name_c)


if __name__ == '__main__':
    unittest.main()
