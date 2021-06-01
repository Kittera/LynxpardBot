import discord
from discord.ext.commands import command, Bot, Cog, Context

import LynxpardBotConfig as Cfg

PREFIX = Cfg.LIST_PREFIXES[1]


class Commands(Cog):
    def __init__(self, client):
        self.client = client

    @command()
    async def commands(self, ctx: Context):
        await send(ctx)


def setup(bot: Bot):
    bot.add_cog(Commands(bot))


async def send(ctx: Context):
    help_embed = discord.Embed(
        title="LynxpardBot Commands",
        color=Cfg.COLOR_ACCENT,
    )

    help_embed.add_field(
        name=f"`{PREFIX}spam, POH TAY TOES, >.>, <.<`",
        value="Canned responses. But there are more...",
        inline=False,
    )

    help_embed.add_field(
        name=f"`{PREFIX}messagecount`",
        value="Per-channel Message Tally Database.",
        inline=False,
    )

    help_embed.add_field(
        name=f"`{PREFIX}timestamp`",
        value="Gives you the timestamp of your request.",
        inline=False,
    )

    help_embed.add_field(
        name=f"`{PREFIX}norris`",
        value="Fetches a random fact about Chuck Norris.",
        inline=False,
    )

    await ctx.send(
        embed=help_embed,
        reference=ctx.message.to_reference(),
        mention_author=False,
    )
