from dataclasses import dataclass
from typing import List

from model.achievement import Achievement
from model.inventory.inventory import Inventory
from model.person import Person
from utils.bot_output_lib import member_not_in_server_error_msg, ADDED_ACHIEVEMENT_TO_SELF_ERROR_MSG


# TODO: test


@dataclass(frozen=True)
class GuildMember:
    """
    A member of a discord guild
    """
    id: str
    display_name: str


class GuildManager:
    """
    Manages a guild
    """

    _guild: Inventory[Person]       # TODO: make read and write to file(s)

    def __init__(self, guild: Inventory[Person]):
        """
        Initializes the class

        :param guild: The guild to manage
        """
        self._guild = guild

    def guild_size(self) -> int:
        """
        :return: The number of people in the guild
        """
        return self._guild.size()

    def guild_contains(self, person_name: str) -> bool:
        """
        :param person_name: The name of person to check the guild for
        :return: True if the person of the given person_name is in the guild; otherwise, False
        """
        return self._guild.contains(person_name)

    def query_guild(self, member: GuildMember, valid_members: List[GuildMember]) -> Person:
        """
        Get the person with the same name as the given member if it is in the guild's given valid_members list; also
        add the given member to the guild if it is not already in the guild but is in the given valid_members list

        :param member: The member with the same name as the member to get
        :param valid_members: The list of members that the given member must be in to be retrieved
        :return: The person with the same name as the given member
        :raise ValueError: If the given member is not in the guild's given valid_members list
        """

        valid_member_ids = [valid_member.id for valid_member in valid_members]

        if member.id not in valid_member_ids:
            raise ValueError(member_not_in_server_error_msg(member.display_name))

        if self._guild.contains(member.id):
            return self._guild.get(member.id)

        person = Person(member.id)
        self._guild.add(person)
        return person

    def add_achievement(self,
                        member: GuildMember,
                        valid_members: List[GuildMember],
                        achievement_name: str,
                        bestower: str):
        """
        Add a new achievement with the given achievement_name to the given member if it is in the given valid_members
        list

        :param member: The member to add the achievement to
        :param valid_members: The list of members that the given member has to be in
        :param achievement_name: The name that the achievement to add to the member has
        :param bestower: The person that instructed the achievement to be bestowed to the given member
        :raise ValueError: If the given member is the given bestower, or if the given member is not in the given
        valid_members list adder
        :raise InventoryContainsItemError: If the given member already contains an achievement that has the given
        achievement_name
        """

        if member.id == bestower:
            raise ValueError(ADDED_ACHIEVEMENT_TO_SELF_ERROR_MSG)

        person = self.query_guild(member, valid_members)
        achievement = Achievement(achievement_name, bestower)
        person.add(achievement)

    def get_achievements(self, member: GuildMember, valid_members: List[GuildMember]) -> List[Achievement]:
        """
        Gets the list of all the achievements that the given member has attained, if the given member is in the given
        valid_members list

        :param member: The member to list the achievements of
        :param valid_members: The list of members that the given member has to be in
        :return: The list of all the achievements that the given member has attained
        :raise ValueError: If the given member is not in the given valid_members list
        """
        person = self.query_guild(member, valid_members)
        return person.get_achievements()
