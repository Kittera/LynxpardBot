from typing import List

import discord

MY_DB_FILE = "LynxpardBotDB/lBotDB"

COLOR_ACCENT = discord.Color.from_rgb(140, 0, 255)

DEFAULT_COGS: List[str] = [
    "LynxpardBotCommands.norris",
]