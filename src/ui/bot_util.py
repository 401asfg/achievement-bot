from typing import List

import discord

from src.model.achievement import Achievement
from src.model.guild_manager import GuildMember
from src.content.bot import member_achievements_header_msg, ACHIEVEMENT_BESTOWER_INDENT


def create_guild_member(member: discord.Member) -> GuildMember:
    """
    :param member: The discord member to create a guild member of
    :return: A guild member created from the given discord member
    """
    return GuildMember(member.id, member.display_name)


def create_guild_members(members: List[discord.Member]) -> List[GuildMember]:
    """
    :param members: The discord members to create guild members from
    :return: A list of guild members that correspond to the given list of discord members
    """
    return [create_guild_member(member) for member in members]


def create_achievement_list_msg(achievements: List[Achievement], guild_member: GuildMember) -> str:
    """
    :param achievements: The list of achievements to create the message from
    :param guild_member: The guild member, that has the given achievements, to include in the message
    :return: A message containing the given achievements and guild_member
    """

    achievement_list_msg = member_achievements_header_msg(guild_member.display_name)

    for achievement in achievements:
        achievement_list_msg += "\n" + achievement.name + "\n" + ACHIEVEMENT_BESTOWER_INDENT + achievement.bestower

    return achievement_list_msg
