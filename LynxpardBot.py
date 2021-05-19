import traceback

import discord

from random import randint

import LynxpardBotConfig
from lBotRandomMessageSets import random_refusal_message
from discord.ext.commands import Bot
from LynxpardBotCommands import ping, messagecount, help, cakeday

MY_DB_FILE = "LynxpardBotDB/lBotDB"

CHANNELS_BEING_COUNTED = []

bot = Bot(command_prefix=['&', ])


@bot.event
async def on_ready():
    print('Loading default cogs...')
    for name in LynxpardBotConfig.DEFAULT_COGS:
        print(load_with_catches(f'{name}'))

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="&commands"))
    print("{0.user} online.".format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content
    chanl = message.channel
    msg_ref = message.to_reference()

    if msg.startswith("&assimilate"):
        await message.reply(f"Hail, Drone#{str(randint(1, 100000000))}")

    if msg == '&commands' or msg == '&help':
        await help.send(message)

    # TODO per-server db-based rules poster configured by message id and using content field of the fetched message

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

    #
    if msg.startswith(("&ping", "&pong")):
        await ping.respond_to_ping(message, bot)

    # surprise happy birthday celebrators
    if 'happy birthday' in str(msg).lower() and len(message.mentions) > 0:
        for name in message.mentions:
            await chanl.send(f'\\o/ Happy Birthday, {name.mention}!')
            await chanl.send(cakeday.ASCII_CAKE)

    if 'happy cake day' in str(msg).lower() and len(message.mentions) > 0:
        for name in message.mentions:
            await chanl.send(f'\\o/ Happy Cake Day, {name.mention}!')
            await chanl.send(cakeday.ASCII_CAKE)

    await bot.process_commands(message)


def load_with_catches(full_name: str, ):
    from discord.ext.commands import ExtensionAlreadyLoaded, ExtensionFailed, ExtensionNotFound, NoEntryPointError
    try:
        bot.load_extension(full_name)
        result = f'{full_name:.<35}cog loaded.'
    except ExtensionNotFound:
        result = f'{full_name:.<35}not found. Nothing will be loaded.'
    except ExtensionAlreadyLoaded:
        result = f'{full_name:.<35}already loaded.'
    except NoEntryPointError:
        result = f'{full_name:.<35}missing setup function.'
    except ExtensionFailed:
        result = f'{full_name:.<35}fatal error during setup.'
        traceback.print_exc()

    return result


with open("botToken.txt") as tokenFile:
    bot.run(tokenFile.readline())
