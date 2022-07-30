import os
import sys

import aiohttp
import discord
import discord.utils
from dotenv import load_dotenv
from discord import Webhook
from discord.ext import commands

load_dotenv()
intents = discord.Intents().all()
intents.members = True
client = commands.Bot(command_prefix=":", intents=intents)
client.remove_command("help")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.offline)
    print(f"Peradaban (Utilities) is ready for action!")


client.run(os.getenv("BOT_TOKEN"))
