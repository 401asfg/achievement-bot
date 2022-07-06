import os
from typing import List

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.bot_output_lib import COMMAND_PREFIX, ACHIEVE_NAME, ACHIEVE_HELP, \
    ACHIEVE_DESCRIPTION, member_already_has_achievement_error_msg, LIST_NAME, \
    LIST_HELP, LIST_DESCRIPTION
from model.guild_manager import GuildManager, GuildMember
from model.inventory.exceptions.inventory_contains_item_error import InventoryContainsItemError
from model.inventory.inventory import Inventory
from model.person import Person

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix=COMMAND_PREFIX)

guild_manager = GuildManager(Inventory[Person]())      # TODO: pass a guild created from a file?


@bot.event
async def on_message(message):
    await bot.process_commands(message)


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


@bot.command(name=ACHIEVE_NAME, help=ACHIEVE_HELP, brief=ACHIEVE_DESCRIPTION)
async def achieve_command(ctx, member: discord.Member, *achievement_name_segments: str):
    guild_member = create_guild_member(member)
    guild_members = create_guild_members(ctx.guild.members)
    achievement_name = " ".join(achievement_name_segments)

    try:
        guild_manager.add_achievement(guild_member, guild_members, achievement_name, ctx.message.author.id)
    except ValueError as e:
        await ctx.send(e)
    except InventoryContainsItemError:
        await ctx.send(member_already_has_achievement_error_msg(guild_member.display_name, achievement_name))


@bot.command(name=LIST_NAME, help=LIST_HELP, brief=LIST_DESCRIPTION)
async def list_command(ctx, member: discord.Member):
    guild_member = create_guild_member(member)
    guild_members = create_guild_members(ctx.guild.members)

    try:
        achievement_list_msg = guild_manager.build_achievement_list_msg(guild_member, guild_members)
        await ctx.send(achievement_list_msg)
    except ValueError as e:
        await ctx.send(e)


bot.run(TOKEN)
