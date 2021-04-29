import sqlite3
from sqlite3 import Error

SQL_NEW_CHAN = '''
INSERT INTO
ChannelMessageCounts(chanID, msgCount, lastCountDate)
VALUES(?, ?, ?)
'''

SQL_GET = '''
SELECT msgCount, lastCountDate
FROM ChannelMessageCounts
WHERE chanID = ?
'''

SQL_CHECK = '''
SELECT EXISTS(Select 1
FROM ChannelMessageCounts
WHERE chanID = ?)
'''

SQL_UPDATE = '''
UPDATE ChannelMessageCounts
SET msgCount = ?, lastCountDate = ?
WHERE chanID = ?
'''


def record_new_channel(conn, channel_id, num_msgs, init_date):
    cur = conn.cursor()
    cur.execute(SQL_NEW_CHAN, (channel_id, num_msgs, init_date))
    conn.commit()


def check_for_channel(conn, channel_id):
    cur = conn.cursor()
    cur.execute(SQL_CHECK, (channel_id,))
    record = cur.fetchone()
    return record[0]


def get(conn, channel_id):
    cur = conn.cursor()
    cur.execute(SQL_GET, (channel_id,))
    row = cur.fetchone()
    return row[0], row[1]


def update_channel_record(conn, new_date, new_message_count, channel_id):
    cur = conn.cursor()
    cur.execute(SQL_UPDATE, (new_message_count, new_date, channel_id))
    conn.commit()


def connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    except Error as e:
        print(e)

    return conn
