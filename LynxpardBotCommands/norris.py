import http.client
import json

from discord.ext.commands import Bot, Cog, Context, command

import LynxpardBotConfig


class Norris(Cog):
    def __init__(self, client: Bot):
        self.client = client

    @command()
    async def norris(self, ctx: Context):
        await random_norris_fact(ctx)


def setup(bot: Bot):
    bot.add_cog(Norris(bot))


async def random_norris_fact(ctx: Context):
    conn = http.client.HTTPSConnection("matchilling-chuck-norris-jokes-v1.p.rapidapi.com")

    headers = {
        'accept'         : "application/json",
        'x-rapidapi-key' : LynxpardBotConfig.RAPID_API_KEY,
        'x-rapidapi-host': "matchilling-chuck-norris-jokes-v1.p.rapidapi.com"
    }

    conn.request("GET", "/jokes/random", headers=headers)
    jay_son = json.loads(conn.getresponse().read().decode("utf-8"))

    await ctx.send(content=jay_son['value'],
                   reference=ctx.message.to_reference(),
                   mention_author=False, )
