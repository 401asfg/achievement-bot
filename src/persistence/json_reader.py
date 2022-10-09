import json
from datetime import date
from pathlib import Path
from typing import List

from src.model.achievement import Achievement
from src.model.guild import Guild
from src.model.person import Person


class JsonReader:
    """
    Reads JSON data from a JSON file
    """

    _destination: Path

    def __init__(self, destination: Path):
        """
        Initializes the class

        :param destination: The JSON file from which this reader reads
        """
        self._destination = destination

    def read(self) -> Guild:
        """
        Reads a guild from a JSON file at the destination

        :raise FileNotFoundError: If there is no file at the destination
        :return: The guild that was read from a JSON file
        """

        with open(self._destination, 'r') as f:
            guild_json = json.load(f)
            return self._parse_guild(guild_json)

    @property
    def destination(self) -> Path:
        return self._destination

    @classmethod
    def _parse_guild(cls, json_object: dict) -> Guild:
        """
        Parse a guild from the given json_object

        :param json_object: A JSON object that represents a guild
        :return: The guild represented by the given json_object
        """

        guild: Guild = Guild()
        cls._add_people(guild, json_object)
        return guild

    @classmethod
    def _add_people(cls, guild: Guild, json_object: dict):
        """
        Add the people that are in the given json_object (which represents a guild) to the given guild

        :param guild: The guild to add people to
        :param json_object: The JSON object, that represents a guild, to get the people from
        """

        people_json: List[dict] = json_object[Guild.ITEMS_JSON_KEY]
        [cls._add_person(guild, person_json) for person_json in people_json]

    @classmethod
    def _add_person(cls, guild: Guild, json_object: dict):
        """
        Add the person that is represented by the given json_object to the given guild

        :param guild: The guild to add a person to
        :param json_object: The JSON object, that represents a person, to get the person from
        """

        person: Person = cls._parse_person(json_object)
        guild.add(person)

    @classmethod
    def _parse_person(cls, json_object: dict) -> Person:
        """
        Parse a person from the given json_object

        :param json_object: A JSON object that represents a person
        :return: The person represented by the given json_object
        """

        name: str = json_object[Person.NAME_JSON_KEY]
        person: Person = Person(name)
        cls._add_achievements(person, json_object)
        return person

    @classmethod
    def _add_achievements(cls, person: Person, json_object: dict):
        """
        Add the achievements that are in the given json_object (which represents a person) to the given person

        :param person: The person to add achievements to
        :param json_object: The JSON object, that represents a person, to get the achievements from
        """

        achievements_json: List[dict] = json_object[Person.ITEMS_JSON_KEY]
        [cls._add_achievement(person, achievement_json) for achievement_json in achievements_json]

    @classmethod
    def _add_achievement(cls, person: Person, json_object: dict):
        """
        Add the achievement that is represented by the given json_object to the given person

        :param person: The person to add an achievement to
        :param json_object: The JSON object, that represents an achievement, to get the achievement from
        """

        achievement: Achievement = cls._parse_achievement(json_object)
        person.add(achievement)

    @classmethod
    def _parse_achievement(cls, json_object: dict) -> Achievement:
        """
        Parse an achievement from the given json_object

        :param json_object: A JSON object that represents an achievement
        :return: The achievement represented by the given json_object
        """

        name: str = json_object[Achievement.NAME_JSON_KEY]
        bestower: str = json_object[Achievement.BESTOWER_JSON_KEY]
        date_achieved: date = json_object[Achievement.DATE_ACHIEVED_JSON_KEY]
        return Achievement(name, bestower, date_achieved)
