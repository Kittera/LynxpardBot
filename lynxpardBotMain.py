import asyncio
import discord

from random import randint
from lBotRandomMessageSets import random_refusal_message
from LynxpardBotCommands import ping, messagecount

MY_DB_FILE = "LynxpardBotDB/lBotDB"

CHANNELS_BEING_COUNTED = []

bot = discord.Client()


@bot.event
async def on_ready():
    await asyncio.sleep(3.0)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="&commands"))
    print("{0.user} online.".format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content
    chanl = message.channel
    msg_ref = message.to_reference()

    if msg.startswith(("&ping", "&pong")):
        await ping.respond_to_ping(message, bot)

    if msg.startswith("&assimilate"):
        drone_id = str(randint(1, 10000))
        await message.reply("Hail, Drone#{0}".format(drone_id))

    if bot.user.mentioned_in(message) and not message.mention_everyone:
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
        await messagecount.report_msg_count(message, CHANNELS_BEING_COUNTED)

with open("botToken.txt") as tokenFile:
    bot.run(tokenFile.readline())
