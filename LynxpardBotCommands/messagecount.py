import discord.abc
from discord_slash import SlashContext, cog_ext

from LynxpardBotDB import lBotMsgCountDB as msgCountDB
import LynxpardBotConfig as Cfg
from contextlib import closing
from discord.ext.commands import Cog, Bot, Context, command


class MessageCount(Cog):
    def __init__(self, client):
        self.client = client
        self.CHANNELS_BEING_COUNTED = []

    @command()
    async def messagecount(self, ctx: Context):
        await ctx.send(
            await report_msg_count(
                ctx=ctx,
                current_counting_list=self.CHANNELS_BEING_COUNTED,
            )
        )

    @cog_ext.cog_slash(
        name="messagecount",
        description="Runs a count of messages in the current channel's history.",
        guild_ids=Cfg.SLASH_GUILD_IDS,
    )
    async def _messagecount(self, ctx: SlashContext):
        await ctx.defer()


def setup(bot: Bot):
    bot.add_cog(MessageCount(bot))


async def report_msg_count(ctx: Context, current_counting_list):
    if not isinstance(ctx.channel, discord.TextChannel):
        return

    if isinstance(ctx, SlashContext):
        await ctx.defer()

    chanl: discord.TextChannel = ctx.channel

    print(f"Message count initiated in channel {chanl.name}")
    with closing(msgCountDB.connection(Cfg.MY_DB_FILE)) as db:
        channel_has_previous_count = msgCountDB.check_for_channel(db, chanl.id)

        output: str = ""
        if chanl.id not in current_counting_list and channel_has_previous_count:
            current_counting_list.append(chanl.id)
            count_data = msgCountDB.get(db, chanl.id)
            new_count = 0
            stamp = str(count_data[1])

            with chanl.typing():
                async for _ in chanl.history(limit=None, after=count_data[1]):
                    new_count += 1
                new_total = count_data[0] + new_count
                msgCountDB.update_channel_record(
                    db, ctx.message.created_at, new_total, chanl.id
                )
                output += (
                    f"{chanl.mention} has {new_count} new messages. \n"
                    f"Last Count: {stamp:19} UTC\n"
                    f"New total is {new_total}."
                )
            current_counting_list.remove(chanl.id)

        elif chanl.id in current_counting_list:
            output += "Patience!"

        else:
            current_counting_list.append(chanl.id)
            await ctx.channel.send(
                content="No previous counts have been done in this channel. I'll have to get back to you."
            )

            init_count = 0
            with chanl.typing():
                async for _ in chanl.history(limit=None):
                    init_count += 1
                msgCountDB.record_new_channel(
                    db,
                    channel_id=chanl.id,
                    num_msgs=init_count,
                    init_date=ctx.message.created_at,
                )
                output += f"I'm back. So far, {chanl.mention} has {init_count} messages as of the time of your request."
                current_counting_list.remove(chanl.id)

        return output
