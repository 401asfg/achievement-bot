from typing import List

import discord

from bot_output_lib import member_not_in_server_error_msg, member_achievements_header_msg
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

    def query_guild(self, member: discord.Member, members: List[discord.Member]) -> Member:
        """
        Get the guild member with the same id as the given member if it is in the given members list; also add the
        given member to the guild if it is not already in the guild but is in the given members list

        :param member: The member with the same id as the member to get
        :param members: The list of members that the given member must be in to be retrieved
        :return: The member with the same id as the given member
        :raise ValueError: If the given member is not in the given members list
        """

        if member not in members:
            raise ValueError(member_not_in_server_error_msg(member.nick))

        if self._guild.contains(member.id):
            return self._guild.get(member.id)

        guild_member = Member(member.id)
        self._guild.add(guild_member)
        return guild_member

    def add_achievement(self, member: discord.Member, members: List[discord.Member], achievement_name: str):
        """
        Add a new achievement with the given achievement_name to the given member if it is in the given members list

        :param member: The member to add the achievement to
        :param members: The members list that the given member has to be in
        :param achievement_name: The name that the achievement to add to the member has
        :raise ValueError: If the given member is not in the given members list
        :raise InventoryContainsItemError: If the given member already contains an achievement that has the given
        achievement_name
        """
        guild_member = self.query_guild(member, members)
        achievement = Achievement(achievement_name)
        guild_member.add(achievement)

    def build_achievement_list_msg(self, member: discord.Member, members: List[discord.Member]) -> str:
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
        achievement_list_msg = member_achievements_header_msg(member.nick)

        for achievement_name in achievement_names:
            achievement_list_msg += "\n" + achievement_name

        return achievement_list_msg
