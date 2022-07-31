# TODO: test

from src.model.guild import Guild

from src.persistence.json_reader import JsonReader
from src.persistence.json_writer import JsonWriter


class GuildSaveSystem:
    """
    Saves and loads a guild
    """

    JSON_STORE = ""

    _json_writer: JsonWriter
    _json_reader: JsonReader

    def __init__(self):
        """
        Initializes the class
        """
        self._json_writer = JsonWriter(self.JSON_STORE)
        self._json_reader = JsonReader(self.JSON_STORE)

    def save(self, guild: Guild):
        """
        Saves the given guild to a JSON file located at JSON_STORE

        :param guild: The guild to save
        """
        self._json_writer.write(guild)

    def load(self) -> Guild:
        """
        Loads a guild from a JSON file located at JSON_Store

        :return: The guild that was loaded
        """
        return self._json_reader.read()
