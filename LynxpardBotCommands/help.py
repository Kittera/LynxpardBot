import discord

import LynxpardBotConfig

PREFIX = '&'


async def send(help_message):
    help_embed = discord.Embed(title='LynxpardBot Commands', color=LynxpardBotConfig.COLOR_ACCENT)

    help_embed.add_field(name=f'`{PREFIX}spam, POH TAY TOES, >.>, <.<`',
                         value='Canned responses. But there are more...',
                         inline=False)

    help_embed.add_field(name=f'`{PREFIX}messagecount`',
                         value='Per-channel Message Tally Database.',
                         inline=False)

    help_embed.add_field(name=f'`{PREFIX}timestamp`',
                         value='Gives you the timestamp of your request.',
                         inline=False)

    help_embed.add_field(name=f'`{PREFIX}norris`',
                         value='Fetches a random fact about Chuck Norris.',
                         inline=False)

    help_embed.add_field(name=f'`{PREFIX}shorten`',
                         value='Shorten a URL.',
                         inline=False)

    await help_message.channel.send(embed=help_embed,
                                    reference=help_message.to_reference(),
                                    mention_author=False)
