from dataclasses import dataclass
from typing import List

from src.content.error_messages import ADDED_ACHIEVEMENT_TO_SELF_ERROR_MSG, member_not_in_server_error_msg
from src.model.achievement import Achievement
from src.model.guild import Guild
from src.model.person import Person


@dataclass(frozen=True)
class GuildMember:
    """
    A member of a discord guild
    """
    name: str
    display_name: str


class GuildManager:
    """
    Manages a guild
    """

    @staticmethod
    def query_guild(guild: Guild, member: GuildMember, valid_members: List[GuildMember]) -> Person:
        """
        Get the person with the same name as the given member if it is in the given guild's given valid_members list;
        also add the given member to the guild if it is not already in the guild but is in the given valid_members list

        :param guild: The guild to query
        :param member: The member with the same name as the member to get
        :param valid_members: The list of members that the given member must be in to be retrieved
        :return: The person with the same name as the given member
        :raise ValueError: If the given member is not in the guild's given valid_members list
        """

        valid_member_names = [valid_member.name for valid_member in valid_members]

        if member.name not in valid_member_names:
            raise ValueError(member_not_in_server_error_msg(member.display_name))

        if guild.contains(member.name):
            return guild.get(member.name)

        person = Person(member.name)
        guild.add(person)
        return person

    @classmethod
    def get_achievements(cls,
                         guild: Guild,
                         member: GuildMember,
                         valid_members: List[GuildMember]) -> List[Achievement]:
        """
        Gets the list of all the achievements that the given member in the given guild has attained, if the given
        member is in the given valid_members list

        :param guild: The guild to get the achievements of its given member
        :param member: The member to list the achievements of
        :param valid_members: The list of members that the given member has to be in
        :return: The list of all the achievements that the given member has attained
        :raise ValueError: If the given member is not in the given valid_members list
        """
        person = cls.query_guild(guild, member, valid_members)
        return person.get_achievements()

    @classmethod
    def add_achievement(cls,
                        guild: Guild,
                        member: GuildMember,
                        valid_members: List[GuildMember],
                        achievement: Achievement):
        """
        Add a new achievement with the given achievement_name to the given member in the given guild if it is in the
        given valid_members list

        :param guild: The guild to add the given achievement to its given member
        :param member: The member to add the achievement to
        :param valid_members: The list of members that the given member has to be in
        :param achievement: The achievement to add to the person in the guild that corresponds to the given member
        :raise ValueError: If the given member is the given bestower, or if the given member is not in the given
        valid_members list adder
        :raise InventoryContainsItemError: If the given member already contains an achievement that has the given
        achievement_name
        """

        if member.name == achievement.bestower:
            raise ValueError(ADDED_ACHIEVEMENT_TO_SELF_ERROR_MSG)

        person = cls.query_guild(guild, member, valid_members)
        person.add(achievement)
