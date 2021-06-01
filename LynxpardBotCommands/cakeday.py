import discord
from discord.ext.commands import Bot, Cog


def ascii_cake(name: str):
    return f'''
```
                         )\\
                        (__)
                         /\\
                        [[]]
                     @@@[[]]@@@
               @@@@@@@@@[[]]@@@@@@@@@
           @@@@@@@      [[]]      @@@@@@@
       @@@@@@@@@        [[]]        @@@@@@@@@
      @@@@@@@           [[]]           @@@@@@@
      !@@@@@@@@@                    @@@@@@@@@!
      !    @@@@@@@                @@@@@@@    !
      !        @@@@@@@@@@@@@@@@@@@@@@        !
      !              @@@@@@@@@@@             !
      !                                      !
      !{name:^38}!
      !                                      !
      !!!!!!!                          !!!!!!!
           !!!!!!!                !!!!!!!
               !!!!!!!!!!!!!!!!!!!!!!!
```
'''


class CakeDay(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.client.user == message.author or message.author.bot:
            return

        msg = message.content
        celebrate = message.channel.send

        if 'happy birthday' in str(msg).lower() and len(message.mentions) > 0:
            for name in message.mentions:
                await celebrate(f'\\o/ Happy Birthday, {name.mention}!')

        if 'happy cake day' in str(msg).lower() and len(message.mentions) > 0:
            for name in message.mentions:
                user: discord.User = name
                await celebrate(f'\\o/ Happy Cake Day, {name.mention}!\n{ascii_cake(user.display_name)}')


def setup(bot: Bot):
    bot.add_cog(CakeDay(bot))
