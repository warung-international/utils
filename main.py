import os
import sys
import discord
import logging
import datetime

from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient

load_dotenv()
intents = discord.Intents().all()
intents.members = True
client = discord.Client(intents=intents)

cluster = MongoClient(os.getenv("MONGODB_URL"))

levelling = cluster["dagelan"]["levelling"]


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    logging.info(f"Peradaban (Utilities) is ready for action!")


@client.event
async def on_user_update(before, after):
    guild = client.get_guild(os.getenv("GUILD_ID"))
    channel = guild.get_channel(os.getenv("CHANNEL_ID"))
    if guild.get_member(before.id):
        if not before.bot:
            if before.display_avatar != after.display_avatar:
                stats = levelling.find_one({"id": before.id})
                if stats is not None:
                    levelling.update_one(
                        {"id": before.id},
                        {"$set": {"image_url": str(after.display_avatar)}},
                    )
                embed = discord.Embed(
                    description=f"{before.mention} **Avatar Changed**",
                    colour=discord.Colour.blurple(),
                )
                embed.set_author(
                    name=f"{before.name}#{before.discriminator}",
                    icon_url=before.display_avatar,
                    url=f"https://discord.com/users/{before.id}",
                )
                embed.set_thumbnail(url=after.display_avatar)
                embed.add_field(
                    name=f"Avatar",
                    value=f"[`before`]({before.display_avatar}) -> [`after`]({after.display_avatar})",
                    inline=True,
                )
                embed.set_footer(text=f"ID: {before.id}")
                embed.timestamp = datetime.datetime.utcnow()
                await channel.send(embed=embed)

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
                    icon_url=after.display_avatar,
                    url=f"https://discord.com/users/{before.id}",
                )
                embed.set_thumbnail(url=after.display_avatar)
                embed.add_field(name=f"Before:", value=f"`{before.name}`", inline=True)
                embed.add_field(name=f"After:", value=f"`{after.name}`", inline=True)
                embed.set_footer(text=f"ID: {before.id}")
                embed.timestamp = datetime.datetime.utcnow()
                await channel.send(embed=embed)

            if before.discriminator != after.discriminator:
                stats = levelling.find_one({"id": before.id})
                if stats is not None:
                    levelling.update_one(
                        {"id": before.id},
                        {"$set": {"discrim": after.discriminator}},
                    )
                embed = discord.Embed(
                    description=f"{before.mention} **Discriminator Changed**",
                    colour=discord.Colour.blurple(),
                )
                embed.set_author(
                    name=f"{before.name}#{before.discriminator}",
                    icon_url=after.display_avatar,
                    url=f"https://discord.com/users/{before.id}",
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
                await channel.send(embed=embed)


client.run(os.getenv("BOT_TOKEN"))
