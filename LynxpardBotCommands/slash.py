import asyncio
from typing import List

import discord
from discord.ext.commands import Cog, Bot
from discord_slash import cog_ext, SlashContext

import LynxpardBotConfig as Cfg


class Slash(Cog):
    def __init__(self, client: Bot):
        self.client = client

    @cog_ext.cog_slash(
        name="test",
        description="Test slash please ignore",
        guild_ids=Cfg.SLASH_GUILD_IDS,
    )
    async def _test(self, ctx: SlashContext):
        embed_list: List[discord.Embed] = [
            discord.Embed(title="Slash Commands", color=Cfg.COLOR_ACCENT),
            discord.Embed(title="Are", color=Cfg.COLOR_ACCENT),
            discord.Embed(title="Nifty", color=Cfg.COLOR_ACCENT),
        ]
        await ctx.send(content="test", embeds=embed_list)

    @cog_ext.cog_slash(
        name="think",
        description="What thinking bots look like.",
    )
    async def _think(self, ctx: SlashContext):
        await ctx.defer()
        timeout = 30.0
        await asyncio.sleep(timeout)
        await ctx.send(f"How thoughtful of me. ({timeout} seconds passed.)")


def setup(bot: Bot):
    bot.add_cog(Slash(bot))
