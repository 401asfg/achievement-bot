from typing import List

from bot_output_lib import member_not_in_server_error_msg, member_achievements_header_msg, \
    ADDED_ACHIEVEMENT_TO_SELF_ERROR_MSG
from model.achievement import Achievement
from model.guild import Guild
from model.member import Member

# TODO: test


class GuildManager:
    """
    Manages a guild
    """

    _guild: Guild               # TODO: make read and write to file(s)

    def __init__(self, guild: Guild):
        """
        Initializes the class

        :param guild: The guild to manage
        """
        self._guild = guild

    def guild_size(self) -> int:
        """
        :return: The number of members in the guild
        """
        return self._guild.size()

    def guild_contains(self, member: str) -> bool:
        """
        :param member: The member to check the guild for
        :return: True if the given member is in the guild; otherwise, False
        """
        return self._guild.contains(member)

    def query_guild(self, member: str, members: List[str]) -> Member:
        """
        Get the guild member with the same name as the given member if it is in the given members list; also add the
        given member to the guild if it is not already in the guild but is in the given members list

        :param member: The member with the same name as the member to get
        :param members: The list of members that the given member must be in to be retrieved
        :return: The member with the same name as the given member
        :raise ValueError: If the given member is not in the given members list
        """

        if member not in members:
            raise ValueError(member_not_in_server_error_msg(member))

        if self._guild.contains(member):
            return self._guild.get(member)

        guild_member = Member(member)
        self._guild.add(guild_member)
        return guild_member

    def add_achievement(self, member: str, members: List[str], achievement_name: str, adder: str):
        """
        Add a new achievement with the given achievement_name to the given member if it is in the given members list

        :param member: The member to add the achievement to
        :param members: The members list that the given member has to be in
        :param achievement_name: The name that the achievement to add to the member has
        :param adder: The member that instructed the achievement to be added to the given member
        :raise ValueError: If the given member is the given, or if the given member is not in the given members list
        adder
        :raise InventoryContainsItemError: If the given member already contains an achievement that has the given
        achievement_name
        """

        if member == adder:
            raise ValueError(ADDED_ACHIEVEMENT_TO_SELF_ERROR_MSG)

        guild_member = self.query_guild(member, members)
        achievement = Achievement(achievement_name)
        guild_member.add(achievement)

    def build_achievement_list_msg(self, member: str, members: List[str]) -> str:
        """
        Builds a message that lists all the achievement that the given member has attained, if the given member is in
        the given members list

        :param member: The member to list the achievements of
        :param members: The members list that the given member has to be in
        :return: The message that lists all the achievements that the given member has attained
        :raise ValueError: If the given member is not in the given members list
        """

        guild_member = self.query_guild(member, members)
        achievement_names = guild_member.get_achievement_names()
        achievement_list_msg = member_achievements_header_msg(member)

        for achievement_name in achievement_names:
            achievement_list_msg += "\n" + achievement_name

        return achievement_list_msg
