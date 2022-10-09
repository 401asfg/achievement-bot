import unittest
from datetime import date
from pathlib import Path

from src.model.achievement import Achievement
from src.model.guild import Guild
from src.model.person import Person
from src.persistence.json_reader import JsonReader


class TestJsonReader(unittest.TestCase):
    TEST_DATA_DIR = (Path() / "../data/test").absolute()
    DESTINATION_DIR = TEST_DATA_DIR / "test_json_reader_data.json"

    json_reader: JsonReader

    def setUp(self) -> None:
        self.json_reader = JsonReader(self.DESTINATION_DIR)

    def test_init(self):
        self.assertEqual(self.DESTINATION_DIR, self.json_reader.destination)

    def test_read(self):
        try:
            json_reader_fail = JsonReader(self.TEST_DATA_DIR / "test_json_reader_data_non_existent")
            json_reader_fail.read()
            self.fail()
        except FileNotFoundError:
            pass

        achievement_name_a = "Achievement A"
        achievement_bestower_a = "Bestower A"
        achievement_date_achieved_a = date(1000, 2, 1)
        expected_achievement_a = Achievement(achievement_name_a, achievement_bestower_a, achievement_date_achieved_a)

        achievement_name_b = "Achievement B"
        achievement_bestower_b = "Bestower B"
        achievement_date_achieved_b = date(2000, 4, 3)
        expected_achievement_b = Achievement(achievement_name_b, achievement_bestower_b, achievement_date_achieved_b)

        person_name_a = "Person A"
        expected_person_a = Person(person_name_a)
        expected_person_a.add(expected_achievement_a)

        person_name_b = "Person B"
        expected_person_b = Person(person_name_b)
        expected_person_b.add(expected_achievement_b)
        expected_person_b.add(expected_achievement_a)

        expected_guild = Guild()
        expected_guild.add(expected_person_a)
        expected_guild.add(expected_person_b)

        actual_guild = self.json_reader.read()
        self.assertEqual(expected_guild.to_json(), actual_guild.to_json())
