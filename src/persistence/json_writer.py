import json
from pathlib import Path

from src.model.guild import Guild


class JsonWriter:
    """
    Writes JSON data to a JSON file
    """

    _destination: Path

    def __init__(self, destination: Path):
        """
        Initializes the class

        :param destination: The JSON file to which this writer writes
        """
        self._destination = destination

    def write(self, guild: Guild):
        """
        Writes the given guild to a JSON file at the destination; creates a file at the destination if it does not
        already exist and writes to it

        :param guild: The guild to write to a JSON file
        """

        with open(self._destination, 'w+') as f:
            guild_json = guild.to_json()
            json.dump(guild_json, f)

    @property
    def destination(self) -> Path:
        return self._destination
