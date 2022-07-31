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
from src.ui.bot_util import create_guild_member, create_guild_members, create_achievement_list_msg

guild_manager = GuildManager()
guild_save_system = GuildSaveSystem()
guild = guild_save_system.load()

load_dotenv()

intents = discord.Intents.default()
intents.members = True

TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.command(name=ACHIEVE_NAME, help=ACHIEVE_HELP, brief=ACHIEVE_DESCRIPTION)
async def achieve_command(ctx, member: discord.Member, *achievement_name_segments: str):
    guild_member = create_guild_member(member)
    valid_guild_members = create_guild_members(ctx.guild.members)

    achievement_name = " ".join(achievement_name_segments)
    achievement = Achievement(achievement_name, ctx.message.author.id)

    # TODO: remove this test code
    await ctx.send('Valid Guild Members:')
    [await ctx.send({valid_guild_member.display_name}) for valid_guild_member in valid_guild_members]

    try:
        guild_manager.add_achievement(guild, guild_member, valid_guild_members, achievement)
        await ctx.send(member_received_achievement_msg(guild_member.display_name, achievement_name))
        guild_save_system.save(guild)
    except ValueError as e:
        await ctx.send(e)
    except InventoryContainsItemError:
        await ctx.send(member_already_has_achievement_error_msg(guild_member.display_name, achievement_name))


@bot.command(name=LIST_NAME, help=LIST_HELP, brief=LIST_DESCRIPTION)
async def list_command(ctx, member: discord.Member):
    guild_member = create_guild_member(member)
    valid_guild_members = create_guild_members(ctx.guild.members)

    # TODO: remove this test code
    await ctx.send('Valid Guild Members:')
    [await ctx.send({valid_guild_member.display_name}) for valid_guild_member in valid_guild_members]

    try:
        achievements = guild_manager.get_achievements(guild, guild_member, valid_guild_members)
        achievement_list_msg = create_achievement_list_msg(achievements, guild_member)
        await ctx.send(achievement_list_msg)
        guild_save_system.save(guild)
    except ValueError as e:
        await ctx.send(e)


bot.run(TOKEN)
