import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from src.content.bot import COMMAND_PREFIX, ACHIEVE_NAME, ACHIEVE_HELP, ACHIEVE_DESCRIPTION, LIST_NAME, LIST_HELP, \
    LIST_DESCRIPTION, member_received_achievement_msg
from src.content.error_messages import member_already_has_achievement_error_msg
from src.model.achievement import Achievement
from src.model.guild_manager import GuildManager
from src.model.inventory.exceptions.inventory_contains_item_error import InventoryContainsItemError
from src.persistence.guild_save_system import GuildSaveSystem
from src.ui.bot_util import create_guild_member, create_guild_members, create_achievement_list_msg, send_msg


_guild_manager = GuildManager()
_guild_save_system = GuildSaveSystem()
_guild = _guild_save_system.load()

load_dotenv()

# TODO: does the member_content intent need to be enabled?

_intents = discord.Intents.default()
_intents.members = True

TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=_intents)


@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


# TODO: pull contents of command functions into model section so these functions have minimal code in them?


@bot.command(name=ACHIEVE_NAME, help=ACHIEVE_HELP, brief=ACHIEVE_DESCRIPTION)
async def achieve_command(ctx, member: discord.Member, *achievement_name_segments: str):
    guild_member = create_guild_member(member)
    valid_guild_members = create_guild_members(ctx.guild.members)

    achievement_name = " ".join(achievement_name_segments)

    try:
        achievement = Achievement(achievement_name, ctx.message.author.name)
        _guild_manager.add_achievement(_guild, guild_member, valid_guild_members, achievement)
        await send_msg(ctx, member_received_achievement_msg(guild_member.display_name, achievement_name))
        _guild_save_system.save(_guild)
    except ValueError as e:
        await send_msg(ctx, str(e))
    except InventoryContainsItemError:
        await send_msg(ctx, member_already_has_achievement_error_msg(guild_member.display_name, achievement_name))


@bot.command(name=LIST_NAME, help=LIST_HELP, brief=LIST_DESCRIPTION)
async def list_command(ctx, member: discord.Member):
    guild_member = create_guild_member(member)
    valid_guild_members = create_guild_members(ctx.guild.members)

    try:
        achievements = _guild_manager.get_achievements(_guild, guild_member, valid_guild_members)
        achievement_list_msg = create_achievement_list_msg(achievements, guild_member)
        await send_msg(ctx, achievement_list_msg)
        _guild_save_system.save(_guild)
    except ValueError as e:
        await send_msg(ctx, str(e))
