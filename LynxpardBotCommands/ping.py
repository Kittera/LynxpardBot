from contextlib import closing
from LynxpardBotDB import lBotPingCountDB as pingDB
from LynxpardBotConfig import MY_DB_FILE


async def respond_to_ping(message, bot):
    msg = message.content
    chanl = message.channel
    author = message.author
    msg_ref = message.to_reference()

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
