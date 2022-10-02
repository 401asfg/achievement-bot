import unittest
import shutil
from pathlib import Path

from src.model.achievement import Achievement
from src.model.guild import Guild
from src.model.person import Person
from src.persistence.guild_save_system import GuildSaveSystem


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

    achievement_b: Achievement
    ACHIEVEMENT_B_NAME = "Achievement B"

    achievement_c: Achievement
    ACHIEVEMENT_C_NAME = "Achievement C"

    achievement_d: Achievement
    ACHIEVEMENT_D_NAME = "Achievement D"

    def setUp(self) -> None:
        self.guild_save_system = GuildSaveSystem()

        self.guild = Guild()

        self.person_a = Person(self.PERSON_A_NAME)
        self.person_b = Person(self.PERSON_B_NAME)
        self.person_c = Person(self.PERSON_C_NAME)

        self.achievement_a = Achievement(self.ACHIEVEMENT_A_NAME, self.PERSON_C_NAME)
        self.achievement_b = Achievement(self.ACHIEVEMENT_B_NAME, self.PERSON_A_NAME)
        self.achievement_c = Achievement(self.ACHIEVEMENT_C_NAME, self.PERSON_B_NAME)
        self.achievement_d = Achievement(self.ACHIEVEMENT_D_NAME, self.PERSON_A_NAME)

        self.person_a.add(self.achievement_a)
        self.person_a.add(self.achievement_c)

        self.person_b.add(self.achievement_b)

        self.person_c.add(self.achievement_b)
        self.person_c.add(self.achievement_c)
        self.person_c.add(self.achievement_d)

    def copy_guild_json(self):
        shutil.copy(self.guild_save_system.JSON_STORE, self.COPY_PATH)

    def test_save(self):
        self.copy_guild_json()
        # TODO: finish

    def test_load(self):
        pass
        # TODO: finish


if __name__ == '__main__':
    unittest.main()
