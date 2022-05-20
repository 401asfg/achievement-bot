import discord
from dotenv import load_dotenv
import os

from command import is_command, interpret_command, exceptions

load_dotenv()
TOKEN = os.getenv('TOKEN')  # TODO: copy bot token into .env file

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content

    if not is_command(content):
        return

    try:
        interpret_command(content, message.author.achievement_name)
    except exceptions.LexError:
        pass                # TODO: send error message to user
    except exceptions.ParsingError:
        pass                # TODO: send error message to user


client.run(TOKEN)
