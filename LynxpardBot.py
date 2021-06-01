import traceback

import discord
from discord.ext.commands import Bot
from discord_slash import SlashCommand

from LynxpardBotConfig import LYNXPARDBOT_TOKEN as BOT_TOKEN, DEFAULT_COGS, LIST_PREFIXES

MY_DB_FILE = "LynxpardBotDB/lBotDB"

bot = Bot(command_prefix=LIST_PREFIXES)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)


@bot.event
async def on_ready():
    print('Loading default cogs...')
    for name in DEFAULT_COGS:
        print(load_with_catches(f'{name}'))

    print("Syncing slash commands...")
    await slash.sync_all_commands()

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="&commands"))
    print("{0.user} online.".format(bot))


def load_with_catches(full_name: str, ):
    from discord.ext.commands import ExtensionAlreadyLoaded, ExtensionFailed, ExtensionNotFound, NoEntryPointError
    try:
        bot.load_extension(full_name)
        result = f'{full_name:.<40}cog loaded.'
    except ExtensionNotFound:
        result = f'{full_name:.<40}not found. Nothing will be loaded.'
    except ExtensionAlreadyLoaded:
        result = f'{full_name:.<40}already loaded.'
    except NoEntryPointError:
        result = f'{full_name:.<40}missing setup function.'
    except ExtensionFailed:
        result = f'{full_name:.<40}fatal error during setup.'
        traceback.print_exc()

    return result


bot.run(BOT_TOKEN)

# TODO per-server db-based rules poster configured by message id and using content field of the fetched message
