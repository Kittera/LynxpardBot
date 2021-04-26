import discord

from LynxpardBotDB import lBotPingCountDB as pingDB, lBotMsgCountDB as msgCountDB
from random import randint
from contextlib import closing
from lBotRandomMessageSets import random_refusal_message

MY_DB_FILE = "LynxpardBotDB/lBotDB"

CHANNELS_BEING_COUNTED = []

bot = discord.Client()


@bot.event
async def on_ready():
    print("{0.user} online.".format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content
    chanl = message.channel
    author = message.author
    msg_ref = message.to_reference()

    if msg.startswith(("&ping", "&pong")):
        with closing(pingDB.connection(MY_DB_FILE)) as db:
            lag = str(round(bot.latency * 1000))
            author_id = str(author.id)
            user_has_pinged_before = pingDB.check_for_user(db, author_id)

            if user_has_pinged_before and "clear" not in msg:
                await message.reply(f"My current latency is {lag}ms.")
                total_pings = str(pingDB.get(db, author_id) + 1)
                await chanl.send(f"{author.mention}, you have now pinged me {total_pings} times across all of Discord.")
                pingDB.update_user(db, author_id, total_pings)

            elif user_has_pinged_before and "clear" in msg:
                pingDB.clear_user(db, author_id)
                await chanl.send("Successfully cleared your database entry.")

            elif not user_has_pinged_before and "clear" in msg:
                await chanl.send(content="You're not even registered yet!!!", reference=msg_ref, mention_author=False)

            else:
                await chanl.send(f"My current latency is {lag}ms.", reference=msg_ref, mention_author=False)
                pingDB.register_user(db, author_id)
                await chanl.send(f"Congratulations {author.mention} on your first ping. I've registered you in my "
                                 f"database! Use &ping clear if you wish to wipe my memory.")

    if msg.startswith("&assimilate"):
        drone_id = str(randint(1, 10000))
        await message.reply("Hail, Drone#{0}".format(drone_id))

    if bot.user.mentioned_in(message):
        await chanl.send("_earperk_", reference=msg_ref, mention_author=False)

    if msg == "POH TAY TOES":
        await chanl.send("Boil 'em, mash 'em, stick 'em in a stew!", reference=msg_ref, mention_author=False)

    if msg == ">.>":
        await chanl.send("<.<")
    if msg == "<.<":
        await chanl.send(">.>")

    if msg.startswith("&spam"):
        await message.reply(random_refusal_message())

    if msg.startswith("&timestamp"):
        await message.reply(str(message.created_at))

    # per-channel message history count
    if msg.startswith("&messagecount"):
        with closing(msgCountDB.connection(MY_DB_FILE)) as db:
            channel_has_previous_count = msgCountDB.check_for_channel(db, chanl.id)

            if chanl.id not in CHANNELS_BEING_COUNTED and channel_has_previous_count:
                CHANNELS_BEING_COUNTED.append(chanl.id)
                count_data = msgCountDB.get(db, chanl.id)
                new_count = 0
                with chanl.typing():
                    async for _ in chanl.history(limit=None, after=count_data[1]):
                        new_count += 1
                    new_total = count_data[0] + new_count
                    msgCountDB.update_channel_record(db, message.created_at, new_total, chanl.id)
                await message.reply(f"\n{chanl.mention} has {new_count} new messages since my last count. "
                                    f"New total is {new_total}.")
                CHANNELS_BEING_COUNTED.remove(chanl.id)

            elif chanl.id in CHANNELS_BEING_COUNTED:
                await message.reply("Patience!")

            else:
                CHANNELS_BEING_COUNTED.append(chanl.id)
                await message.reply("No previous counts have been done in this channel. I'll have to get back to you.")

                init_count = 0
                with chanl.typing():
                    async for _ in chanl.history(limit=None):
                        init_count += 1
                    msgCountDB.record_new_channel(db, channel_id=chanl.id, num_msgs=init_count,
                                                  init_date=message.created_at)
                    await message.reply(f"I'm back. So far, {chanl.mention} has {init_count} messages as of the time "
                                        f"of your request.")
                    CHANNELS_BEING_COUNTED.remove(chanl.id)

with open("botToken.txt") as tokenFile:
    bot.run(tokenFile.readline())
