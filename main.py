import os
import sys

import aiohttp
import nextcord
import nextcord.utils
from dotenv import load_dotenv
from nextcord import Webhook
from nextcord.ext import commands

load_dotenv()
intents = nextcord.Intents().all()
client = commands.Bot()
client.remove_command("help")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.offline)
    print(f"Utilities is ready for action")


client.run(os.getenv("BOT_TOKEN"))
