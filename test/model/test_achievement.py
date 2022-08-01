import unittest

from src.model.achievement import Achievement


class TestAchievement(unittest.TestCase):
    NAME_A = "Name A"
    NAME_B = "Name B"
    NAME_C = "Name C"

    BESTOWER_A = "Bestower A"
    BESTOWER_B = "Bestower B"
    BESTOWER_C = "Bestower C"

    achievement_a: Achievement
    achievement_b: Achievement
    achievement_c: Achievement

    def setUp(self) -> None:
        self.achievement_a = Achievement(self.NAME_A, self.BESTOWER_A)
        self.achievement_b = Achievement(self.NAME_B, self.BESTOWER_B)
        self.achievement_c = Achievement(self.NAME_C, self.BESTOWER_C)

    def test_init(self):
        def assert_init(expected_name: str, expected_bestower: str, achievement: Achievement):
            self.assertEqual(expected_name, achievement.name)
            self.assertEqual(expected_bestower, achievement.bestower)

        assert_init(self.NAME_A, self.BESTOWER_A, self.achievement_a)
        assert_init(self.NAME_B, self.BESTOWER_B, self.achievement_b)
        assert_init(self.NAME_C, self.BESTOWER_C, self.achievement_c)

    def test_to_json(self):
        def assert_to_json(achievement: Achievement, expected_json: dir):
            actual_achievement = achievement.to_json()
            self.assertEqual(expected_json, actual_achievement)

        assert_to_json(self.achievement_a,
                       {
                           Achievement.NAME_JSON_KEY: self.NAME_A,
                           Achievement.BESTOWER_JSON_KEY: self.BESTOWER_A
                       })

        assert_to_json(self.achievement_b,
                       {
                           Achievement.NAME_JSON_KEY: self.NAME_B,
                           Achievement.BESTOWER_JSON_KEY: self.BESTOWER_B
                       })

        assert_to_json(self.achievement_c,
                       {
                           Achievement.NAME_JSON_KEY: self.NAME_C,
                           Achievement.BESTOWER_JSON_KEY: self.BESTOWER_C
                       })


if __name__ == '__main__':
    unittest.main()
