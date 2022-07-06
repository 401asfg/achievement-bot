import unittest
from typing import Optional

from model.achievement import Achievement


class TestAchievement(unittest.TestCase):
    NAME_A = "Name A"
    NAME_B = "Name B"
    NAME_C = "Name C"

    BESTOWER_A = "Bestower A"
    BESTOWER_B = "Bestower B"
    BESTOWER_C = "Bestower C"

    def test_init(self):
        def assert_init(name: str, bestower: str):
            achievement: Achievement
            achievement = Achievement(name, bestower)
            self.assertEqual(name, achievement.name)

        assert_init(self.NAME_A, self.BESTOWER_A)
        assert_init(self.NAME_B, self.BESTOWER_B)
        assert_init(self.NAME_C, self.BESTOWER_C)


if __name__ == '__main__':
    unittest.main()
