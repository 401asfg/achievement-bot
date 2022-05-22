import os

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


@bot.command(name=ACHIEVE_NAME, help=ACHIEVE_HELP, brief=ACHIEVE_DESCRIPTION)
async def achieve_command(ctx, member: discord.Member, achievement_name: str):
    try:
        guild_manager.add_achievement(member, ctx.guild.members, achievement_name)
    except ValueError:
        await ctx.send(member_not_in_server_error_msg(member.nick))
    except InventoryContainsItemError:
        await ctx.send(member_already_has_achievement_error_msg(member.nick, achievement_name))


@bot.command(name=LIST_NAME, help=LIST_HELP, brief=LIST_DESCRIPTION)
async def list_command(ctx, member: discord.Member):
    try:
        achievement_list_msg = guild_manager.build_achievement_list_msg(member, ctx.guild.members)
        await ctx.send(achievement_list_msg)
    except ValueError:
        await ctx.send(member_not_in_server_error_msg(member.nick))


bot.run(TOKEN)
