from typing import List

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from model.achievement import Achievement
from model.guild import Guild
from model.inventory_exceptions.inventory_contains_item_error import InventoryContainsItemError
from model.member import Member

COMMAND_PREFIX = ";"

ACHIEVE_NAME = "achieve"
ACHIEVE_DESCRIPTION = "Gives a user a custom achievement"
ACHIEVE_EXAMPLE = COMMAND_PREFIX + ACHIEVE_NAME + " @TheMightyMeercat Meercat Killer"
ACHIEVE_HELP = ACHIEVE_DESCRIPTION + "\n" + ACHIEVE_EXAMPLE

LIST_NAME = "list"
LIST_DESCRIPTION = "Lists all of the achievements that a user has"
LIST_EXAMPLE = COMMAND_PREFIX + LIST_NAME + " @TheMightyMeercat"
LIST_HELP = LIST_DESCRIPTION + "\n" + LIST_EXAMPLE

load_dotenv()
TOKEN = os.getenv('TOKEN')  # TODO: copy bot token into .env file
bot = commands.Bot(command_prefix=COMMAND_PREFIX)

guild: Guild        # TODO: make read and write to file(s)


@bot.event
async def on_message(message):
    await bot.process_commands(message)


def member_not_in_server_error_msg(name: str) -> str:
    """
    :param name: The name of the member that is not in the server
    :return: An error message for when a member is not in the server
    """
    return f"{name} is not in this server"


def member_already_has_achievement_error_msg(member_name: str, achievement_name: str) -> str:
    """
    :param member_name: The name of the member
    :param achievement_name: The name of the achievement that the member already has
    :return: An error message for when a member already has an achievement
    """
    return f"{member_name} already has the {achievement_name} achievement"


def query_guild(member: discord.Member, members: List[discord.Member]) -> Member:
    """
    Get the guild member with the same id as the given member if it is in the given members list; also add the given
    member to the guild if it is not already in the guild but is in the given members list

    :param member: The member with the same id as the member to get
    :param members: The list of members that the given member must be in to be retrieved
    :return: The member with the same id as the given member
    :raise ValueError: If the given member is not in the given members list
    """

    if member not in members:
        raise ValueError(member_not_in_server_error_msg(member.nick))

    if guild.contains(member.id):
        return guild.get(member.id)

    guild_member = Member(member.id)
    guild.add(guild_member)
    return guild_member


def add_achievement(member: discord.Member, members: List[discord.Member], achievement_name: str):
    """
    Add a new achievement with the given achievement_name to the given member if it is in the given members list

    :param member: The member to add the achievement to
    :param members: The members list that the given member has to be in
    :param achievement_name: The name that the achievement to add to the member has
    :raise ValueError: If the given member is not in the given members list
    :raise InventoryContainsItemError: If the given member already contains an achievement that has the given
    achievement_name
    """
    guild_member = query_guild(member, members)
    achievement = Achievement(achievement_name)
    guild_member.add(achievement)


@bot.command(name=ACHIEVE_NAME, help=ACHIEVE_HELP, brief=ACHIEVE_DESCRIPTION)
async def achieve_command(ctx, member: discord.Member, achievement_name: str):
    try:
        add_achievement(member, ctx.guild.members, achievement_name)
    except ValueError:
        await ctx.send(member_not_in_server_error_msg(member.nick))
    except InventoryContainsItemError:
        await ctx.send(member_already_has_achievement_error_msg(member.nick, achievement_name))


@bot.command(name=LIST_NAME, help=LIST_HELP, brief=LIST_DESCRIPTION)
async def list_command(ctx, member: discord.Member):
    pass  # TODO: implement


bot.run(TOKEN)
