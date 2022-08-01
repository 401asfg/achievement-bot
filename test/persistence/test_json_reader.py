import os.path
import unittest

from src.model.achievement import Achievement
from src.model.guild import Guild
from src.model.inventory.exceptions.inventory_item_not_found_error import InventoryItemNotFoundError
from src.model.person import Person
from src.persistence.json_reader import JsonReader


class TestJsonReader(unittest.TestCase):
    DESTINATION = os.path.abspath(os.curdir) + "../../data/test/json_reader_test_data.json"

    json_reader: JsonReader

    def setUp(self) -> None:
        self.json_reader = JsonReader(self.DESTINATION)

    def test_init(self):
        self.assertEqual(self.DESTINATION, self.json_reader.destination)

    def test_read(self):
        try:
            json_reader_fail = JsonReader("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            json_reader_fail.read()
            self.fail()
        except IOError:
            pass

        achievement_name_a = "Achievement A"
        achievement_bestower_a = "Bestower A"
        expected_achievement_a = Achievement(achievement_name_a, achievement_bestower_a)

        achievement_name_b = "Achievement B"
        achievement_bestower_b = "Bestower B"
        expected_achievement_b = Achievement(achievement_name_b, achievement_bestower_b)

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
