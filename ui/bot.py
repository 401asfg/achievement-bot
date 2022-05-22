import os
from typing import List

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot_output_lib import COMMAND_PREFIX, member_not_in_server_error_msg, ACHIEVE_NAME, ACHIEVE_HELP, \
    ACHIEVE_DESCRIPTION, member_already_has_achievement_error_msg, LIST_NAME, \
    LIST_HELP, LIST_DESCRIPTION
from model.guild import Guild
from model.guild_manager import GuildManager
from model.inventory.exceptions.inventory_contains_item_error import InventoryContainsItemError

load_dotenv()
TOKEN = os.getenv('TOKEN')  # TODO: copy bot token into .env file
bot = commands.Bot(command_prefix=COMMAND_PREFIX)

guild_manager = GuildManager(Guild())       # TODO: pass a guild created from a file?


@bot.event
async def on_message(message):
    await bot.process_commands(message)


def get_member_ids(members: List[discord.Member]) -> List[str]:
    """
    :param members: The members to get the ids of
    :return: A list of member ids that correspond to the given list of members
    """
    return [member.id for member in members]


@bot.command(name=ACHIEVE_NAME, help=ACHIEVE_HELP, brief=ACHIEVE_DESCRIPTION)
async def achieve_command(ctx, member: discord.Member, achievement_name: str):
    member_id = member.id
    members = get_member_ids(ctx.guild.members)

    try:
        guild_manager.add_achievement(member_id, members, achievement_name)
    except ValueError:
        await ctx.send(member_not_in_server_error_msg(member_id))
    except InventoryContainsItemError:
        await ctx.send(member_already_has_achievement_error_msg(member_id, achievement_name))


@bot.command(name=LIST_NAME, help=LIST_HELP, brief=LIST_DESCRIPTION)
async def list_command(ctx, member: discord.Member):
    member_id = member.id
    members = get_member_ids(ctx.guild.members)

    try:
        achievement_list_msg = guild_manager.build_achievement_list_msg(member_id, members)
        await ctx.send(achievement_list_msg)
    except ValueError:
        await ctx.send(member_not_in_server_error_msg(member_id))


bot.run(TOKEN)
