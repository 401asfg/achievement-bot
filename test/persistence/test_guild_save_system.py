import unittest
import shutil
from datetime import date
from pathlib import Path

from src.model.achievement import Achievement
from src.model.guild import Guild
from src.model.person import Person
from src.persistence.guild_save_system import GuildSaveSystem
from src.persistence.json_writer import JsonWriter


class TestGuildSaveSystem(unittest.TestCase):
    COPY_PATH = (Path() / "../data/test/guild_copy.json").absolute()

    guild_save_system: GuildSaveSystem

    guild: Guild

    person_a: Person
    PERSON_A_NAME = "Person A"

    person_b: Person
    PERSON_B_NAME = "Person B"

    person_c: Person
    PERSON_C_NAME = "Person C"

    achievement_a: Achievement
    ACHIEVEMENT_A_NAME = "Achievement A"
    DATE_ACHIEVED_A = date(1000, 1, 1)

    achievement_b: Achievement
    ACHIEVEMENT_B_NAME = "Achievement B"
    DATE_ACHIEVED_B = date(2000, 2, 2)

    achievement_c: Achievement
    ACHIEVEMENT_C_NAME = "Achievement C"
    DATE_ACHIEVED_C = date(3000, 3, 3)

    achievement_d: Achievement
    ACHIEVEMENT_D_NAME = "Achievement D"
    DATE_ACHIEVED_D = date(4000, 4, 4)

    def setUp(self) -> None:
        self.guild_save_system = GuildSaveSystem()

        self.guild = Guild()

        self.person_a = Person(self.PERSON_A_NAME)
        self.person_b = Person(self.PERSON_B_NAME)
        self.person_c = Person(self.PERSON_C_NAME)

        self.achievement_a = Achievement(self.ACHIEVEMENT_A_NAME, self.PERSON_C_NAME, self.DATE_ACHIEVED_A)
        self.achievement_b = Achievement(self.ACHIEVEMENT_B_NAME, self.PERSON_A_NAME, self.DATE_ACHIEVED_B)
        self.achievement_c = Achievement(self.ACHIEVEMENT_C_NAME, self.PERSON_B_NAME, self.DATE_ACHIEVED_C)
        self.achievement_d = Achievement(self.ACHIEVEMENT_D_NAME, self.PERSON_A_NAME, self.DATE_ACHIEVED_D)

        self.person_a.add(self.achievement_a)
        self.person_a.add(self.achievement_c)

        self.person_b.add(self.achievement_b)

        self.person_c.add(self.achievement_b)
        self.person_c.add(self.achievement_c)
        self.person_c.add(self.achievement_d)

        self.guild.add(self.person_a)
        self.guild.add(self.person_b)
        self.guild.add(self.person_c)

        shutil.move(self.guild_save_system.JSON_STORE, self.COPY_PATH)

    def tearDown(self) -> None:
        shutil.move(self.COPY_PATH, self.guild_save_system.JSON_STORE)

    def test_load(self):
        empty_guild = Guild()
        actual_guild = self.guild_save_system.load()
        self.assertEqual(empty_guild.to_json(), actual_guild.to_json())

        json_writer = JsonWriter(self.guild_save_system.JSON_STORE)
        json_writer.write(self.guild)

        actual_guild = self.guild_save_system.load()
        self.assertEqual(self.guild.to_json(), actual_guild.to_json())

    def test_save(self):
        def assert_save():
            self.guild_save_system.save(self.guild)
            actual_guild = self.guild_save_system.load()
            self.assertEqual(self.guild.to_json(), actual_guild.to_json())

        # Non Existent
        assert_save()

        # Empty Guild
        json_writer = JsonWriter(self.guild_save_system.JSON_STORE)
        guild_to_overwrite = Guild()
        json_writer.write(guild_to_overwrite)
        assert_save()

        # Partial Guild
        person_to_overwrite_a = Person("Person To Overwrite A")
        person_to_overwrite_b = Person("Person To Overwrite B")
        achievement_to_overwrite_a = Achievement("Achievement To Overwrite A", "Other Person", date(2222, 12, 12))
        achievement_to_overwrite_b = Achievement("Achievement To Overwrite B", "Other Person", date(3333, 11, 11))

        person_to_overwrite_a.add(achievement_to_overwrite_a)
        person_to_overwrite_a.add(achievement_to_overwrite_b)
        guild_to_overwrite.add(person_to_overwrite_a)
        guild_to_overwrite.add(person_to_overwrite_b)

        json_writer.write(guild_to_overwrite)
        assert_save()


if __name__ == '__main__':
    unittest.main()
