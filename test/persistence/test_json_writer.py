import os
import unittest

from src.model.achievement import Achievement
from src.model.guild import Guild
from src.model.person import Person
from src.persistence.json_reader import JsonReader
from src.persistence.json_writer import JsonWriter


class TestJsonWriter(unittest.TestCase):
    TEST_DIR_DESTINATION = os.path.abspath(os.curdir) + "../../data/test/"
    DESTINATION = TEST_DIR_DESTINATION + "json_writer_test_data.json"

    ACHIEVEMENT_NAME_A = "Achievement A"
    BESTOWER_A = "Bestower A"

    ACHIEVEMENT_NAME_B = "Achievement B"
    BESTOWER_B = "Bestower B"

    PERSON_NAME_A = "Person A"
    PERSON_NAME_B = "Person B"

    achievement_a: Achievement
    achievement_b: Achievement

    person_a: Person
    person_b: Person

    guild: Guild

    def setUp(self) -> None:
        self.achievement_a = Achievement(self.ACHIEVEMENT_NAME_A, self.BESTOWER_A)
        self.achievement_b = Achievement(self.ACHIEVEMENT_NAME_B, self.BESTOWER_B)

        self.person_a = Person(self.PERSON_NAME_A)
        self.person_a.add(self.achievement_a)

        self.person_b = Person(self.PERSON_NAME_B)
        self.person_b.add(self.achievement_b)
        self.person_b.add(self.achievement_a)

        self.guild = Guild()
        self.guild.add(self.person_a)
        self.guild.add(self.person_b)

    def test_init(self):
        json_writer = JsonWriter(self.DESTINATION)
        self.assertEqual(self.DESTINATION, json_writer.destination)

    def test_write(self):
        def assert_write(destination: str):
            json_writer = JsonWriter(destination)
            json_writer.write(self.guild)

            json_reader = JsonReader(destination)
            actual_guild = json_reader.read()

            actual_guild_json = actual_guild.to_json()
            expected_guild_json = self.guild.to_json()

            self.assertEqual(expected_guild_json, actual_guild_json)

        destination_non_existent = self.TEST_DIR_DESTINATION + "json_writer_test_data_non_existent.json"
        assert_write(destination_non_existent)
        os.remove(destination_non_existent)

        assert_write(self.DESTINATION)


if __name__ == '__main__':
    unittest.main()
