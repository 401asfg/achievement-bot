import unittest
from typing import Optional

from model.achievement import Achievement


class MyTestCase(unittest.TestCase):
    name_a = "Name A"
    name_b = "Name B"
    name_c = "Name C"

    description_a = "Description A"
    description_b = "Description B"

    def test_init(self):
        def assert_init(name: str, description: Optional[str]):
            achievement: Achievement

            if description is not None:
                achievement = Achievement(name, description)
                self.assertEqual(description, achievement.description)
            else:
                achievement = Achievement(name)

            self.assertEqual(name, achievement.name)

        assert_init(self.name_a, self.description_a)
        assert_init(self.name_b, self.description_b)
        assert_init(self.name_c, None)


if __name__ == '__main__':
    unittest.main()
