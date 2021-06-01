from random import randint

import discord
from discord.ext.commands import Bot, Cog, Context, command, is_owner

import LynxpardBotConfig
from lBotRandomMessageSets import random_refusal_message
from LynxpardBotCommands import help


class CannedResponses(Cog):
    def __init__(self, client: Bot):
        self.client = client

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.client.user:
            return

        msg = message.content
        chanl = message.channel
        msg_ref = message.to_reference()

        if msg.startswith("&assimilate"):
            await message.reply(f"Hail, Drone#{str(randint(1, 100000000))}")

        if msg == "POH TAY TOES":
            await chanl.send(
                content="Boil 'em, mash 'em, stick 'em in a stew!",
                reference=msg_ref,
                mention_author=False,
            )

            if msg == "&commands":
                await help.send(message)

        if msg == ">.>":
            await chanl.send("<.<")
        if msg == "<.<":
            await chanl.send(">.>")

        if msg.startswith("&spam"):
            await message.reply(random_refusal_message())

        if msg.startswith("&timestamp"):
            await message.reply(str(message.created_at))

    @command()
    @is_owner()
    async def selfpurge(self, ctx: Context):
        if ctx.author.id == LynxpardBotConfig.ID_DEVELOPER:
            tokens = ctx.message.content.split()

            limit: int
            if len(tokens) == 2 and str(tokens[1]).isnumeric():
                limit: int = int(tokens[1])
            else:
                limit = 100

            async for message in ctx.history(limit=10000):
                if message.author == self.client.user and limit >= 0:
                    await message.delete()
                    limit -= 1


def setup(bot: Bot):
    bot.add_cog(CannedResponses(bot))
