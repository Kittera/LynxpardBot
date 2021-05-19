from LynxpardBotDB import lBotMsgCountDB as msgCountDB
from LynxpardBotConfig import MY_DB_FILE
from contextlib import closing


async def report_msg_count(message, current_counting_list):
    chanl = message.channel
    print(f'Message count initiated in channel {message.channel.mention}')

    with closing(msgCountDB.connection(MY_DB_FILE)) as db:
        channel_has_previous_count = msgCountDB.check_for_channel(db, chanl.id)

        if chanl.id not in current_counting_list and channel_has_previous_count:
            current_counting_list.append(chanl.id)
            count_data = msgCountDB.get(db, chanl.id)
            new_count = 0

            with chanl.typing():
                async for _ in chanl.history(limit=None, after=count_data[1]):
                    new_count += 1
                new_total = count_data[0] + new_count
                msgCountDB.update_channel_record(db, message.created_at, new_total, chanl.id)
            await message.reply(f"\n{chanl.mention} has {new_count} new messages since my last count. "
                                f"New total is {new_total}.")
            current_counting_list.remove(chanl.id)

        elif chanl.id in current_counting_list:
            await message.reply("Patience!")

        else:
            current_counting_list.append(chanl.id)
            await message.reply("No previous counts have been done in this channel. I'll have to get back to you.")

            init_count = 0
            with chanl.typing():
                async for _ in chanl.history(limit=None):
                    init_count += 1
                msgCountDB.record_new_channel(db, channel_id=chanl.id, num_msgs=init_count,
                                              init_date=message.created_at)
                await message.reply(f"I'm back. So far, {chanl.mention} has {init_count} messages as of the time "
                                    f"of your request.")
                current_counting_list.remove(chanl.id)
