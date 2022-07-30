import datetime
import os

import aiohttp
import discord
from dotenv import load_dotenv
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
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
                if stats is not None:
                    levelling.update_one(
                        {"id": before.id},
                        {"$set": {"image_url": str(after.avatar_url)}},
                    )
                embed = discord.Embed(
                    description=f"{before.mention} **Avatar Changed**",
                    colour=discord.Colour.blurple(),
                )
                embed.set_author(
                    name=f"{before.name}#{before.discriminator}",
                    icon_url=before.avatar_url,
                    url=f"https://discord.com/users/{before.id}",
                )
                embed.set_thumbnail(url=after.avatar_url)
                embed.add_field(
                    name=f"Avatar",
                    value=f"[`before`]({before.avatar_url}) -> [`after`]({after.avatar_url})",
                    inline=True,
                )
                embed.set_footer(text=f"ID: {before.id}")
                embed.timestamp = datetime.datetime.utcnow()
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        os.getenv("WEBHOOK_TOKEN"), adapter=AsyncWebhookAdapter(session)
                    )
                    await webhook.send(embed=embed)

            if before.name != after.name:
                stats = levelling.find_one({"id": before.id})
                if stats is not None:
                    levelling.update_one(
                        {"id": before.id}, {"$set": {"username": after.name}}
                    )
                    if after.nick is None:
                        levelling.update_one(
                            {"id": after.id}, {"$set": {"displayname": after.name}}
                        )
                embed = discord.Embed(
                    description=f"{before.mention} **Username Changed**",
                    colour=discord.Colour.blurple(),
                )
                embed.set_author(
                    name=f"{before.name}#{before.discriminator}",
                    icon_url=after.avatar_url,
                    url=f"https://discord.com/users/{before.id}",
                )
                embed.set_thumbnail(url=after.avatar_url)
                embed.add_field(name=f"Before:", value=f"`{before.name}`", inline=True)
                embed.add_field(name=f"After:", value=f"`{after.name}`", inline=True)
                embed.set_footer(text=f"ID: {before.id}")
                embed.timestamp = datetime.datetime.utcnow()
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        os.getenv("WEBHOOK_TOKEN"), adapter=AsyncWebhookAdapter(session)
                    )
                    await webhook.send(embed=embed)

            if before.discriminator != after.discriminator:
                stats = levelling.find_one({"id": before.id})
                if stats is not None:
                    levelling.update_one(
                        {"id": before.id}, {"$set": {"discrim": after.discriminator}}
                    )
                embed = discord.Embed(
                    description=f"{before.mention} **Discriminator Changed**",
                    colour=discord.Colour.blurple(),
                )
                embed.set_author(
                    name=f"{before.name}#{before.discriminator}",
                    icon_url=after.avatar_url,
                    url=f"https://discord.com/users/{before.id}",
                )
                embed.set_thumbnail(url=after.avatar_url)
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
                        os.getenv("WEBHOOK_TOKEN"), adapter=AsyncWebhookAdapter(session)
                    )
                    await webhook.send(embed=embed)


def setup(client):
    client.add_cog(events(client))
