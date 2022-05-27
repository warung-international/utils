import datetime
import os

import aiohttp
import nextcord
from dotenv import load_dotenv
from nextcord import Webhook
from nextcord.ext import commands
from pymongo import MongoClient

load_dotenv()

cluster = MongoClient(os.getenv("MONGODB_URL"))

levelling = cluster["dagelan"]["levelling"]


class events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        guild = self.client.get_guild(922523614828433419)
        if guild.get_member(before.id):
            if before.avatar != after.avatar:
                stats = levelling.find_one({"id": before.id})
                if stats is None:
                    return
                else:
                    levelling.update_one(
                        {"id": before.id},
                        {"$set": {"image_url": str(after.display_avatar)}},
                    )
                embed = nextcord.Embed(
                    description=f"{before.mention} **Avatar Changed**",
                    colour=nextcord.Colour.blurple(),
                )
                embed.set_author(
                    name=f"{before.name}#{before.discriminator}",
                    icon_url=before.display_avatar,
                    url=f"https://discord.com/users/{before.author.id}",
                )
                embed.set_thumbnail(url=after.display_avatar)
                embed.add_field(
                    name=f"Avatar",
                    value=f"[before]({before.display_avatar}) -> [after]({after.display_avatar})",
                    inline=True,
                )
                embed.set_footer(text=f"ID: {before.id}")
                embed.timestamp = datetime.datetime.utcnow()
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        os.getenv("WEBHOOK_TOKEN"), session=session
                    )
                    await webhook.send(embed=embed)

            if before.name != after.name:
                stats = levelling.find_one({"id": before.id})
                if stats is None:
                    return
                else:
                    levelling.update_one(
                        {"id": before.id}, {"$set": {"username": after.name}}
                    )
                embed = nextcord.Embed(
                    description=f"{before.mention} **Username Changed**",
                    colour=nextcord.Colour.blurple(),
                )
                embed.set_author(
                    name=f"{before.name}#{before.discriminator}",
                    icon_url=after.display_avatar,
                    url=f"https://discord.com/users/{before.author.id}",
                )
                embed.set_thumbnail(url=after.display_avatar)
                embed.add_field(name=f"Before:", value=f"`{before.name}`", inline=True)
                embed.add_field(name=f"After:", value=f"`{after.name}`", inline=True)
                embed.set_footer(text=f"ID: {before.id}")
                embed.timestamp = datetime.datetime.utcnow()
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        os.getenv("WEBHOOK_TOKEN"), session=session
                    )
                    await webhook.send(embed=embed)

            if before.discriminator != after.discriminator:
                stats = levelling.find_one({"id": before.id})
                if stats is None:
                    return
                else:
                    levelling.update_one(
                        {"id": before.id}, {"$set": {"discrim": after.discriminator}}
                    )
                embed = nextcord.Embed(
                    description=f"{before.mention} **Discriminator Changed**",
                    colour=nextcord.Colour.blurple(),
                )
                embed.set_author(
                    name=f"{before.name}#{before.discriminator}",
                    icon_url=after.display_avatar,
                    url=f"https://discord.com/users/{before.author.id}",
                )
                embed.set_thumbnail(url=after.display_avatar)
                embed.add_field(
                    name=f"Before:", value=f"`#{before.discriminator}`", inline=True
                )
                embed.add_field(
                    name=f"After:", value=f"`#{after.discriminator}`", inline=True
                )
                embed.set_footer(text=f"ID: {before.id}")
                embed.timestamp = datetime.datetime.utcnow()
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        os.getenv("WEBHOOK_TOKEN"), session=session
                    )
                    await webhook.send(embed=embed)


def setup(client):
    client.add_cog(events(client))
