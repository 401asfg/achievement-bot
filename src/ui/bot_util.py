from typing import List

import discord

from src.content.bot import member_achievement_list_msg, bot_msg, member_no_achievements_msg
from src.model.achievement import Achievement
from src.model.guild_manager import GuildMember


async def send_msg(ctx, msg: str):
    """
    Send the given msg over discord with the given ctx, with bot formatting

    :param ctx: The context of the message
    :param msg: The message to send
    """
    await ctx.send(bot_msg(msg))


def create_guild_member(member: discord.Member) -> GuildMember:
    """
    :param member: The discord member to create a guild member of
    :return: A guild member created from the given discord member
    """
    return GuildMember(member.name, member.display_name)


def create_guild_members(members: List[discord.Member]) -> List[GuildMember]:
    """
    :param members: The discord members to create guild members from
    :return: A list of guild members that correspond to the given list of discord members
    """
    return [create_guild_member(member) for member in members]


# TODO: test/move into model?


def create_achievement_list_msg(achievements: List[Achievement], guild_member: GuildMember) -> str:
    """
    :param achievements: The list of achievements to create the message from
    :param guild_member: The guild member, that has the given achievements, to include in the message
    :return: A message containing the given achievements and guild_member
    """
    member_name = guild_member.display_name

    if not achievements:
        return member_no_achievements_msg(member_name)

    achievement_names = [achievement.name for achievement in achievements]
    bestower_names = [achievement.bestower for achievement in achievements]
    return member_achievement_list_msg(member_name, achievement_names, bestower_names)
