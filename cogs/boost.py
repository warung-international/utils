import time
from datetime import datetime

import discord
from discord.ext import commands

orange = discord.Colour.blurple()


class boost(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.type.name in [
            "premium_guild_subscription",
            "premium_guild_tier_1",
            "premium_guild_tier_2",
            "premium_guild_tier_3",
        ]:
            if message.guild.id == 922523614828433419:
                embed = discord.Embed(
                    colour=orange,
                    description=f"<:booster:914737485924409405> **{message.author.display_name}**, Terima Kasih sudah mem-boost server ini! :pray:",
                )
                embed.set_thumbnail(url=message.author.display_avatar)
                embed.add_field(
                    name="Boosted Since:",
                    value=f"<t:{int(time.time())}:D> (**<t:{int(time.time())}:R>**)",
                    inline=True,
                )
                embed.timestamp = datetime.utcnow()
                channel = self.client.get_channel(922523615377907715)
                await channel.send(embed=embed)


def setup(client):
    client.add_cog(boost(client))
