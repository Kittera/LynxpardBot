import sqlite3
from sqlite3 import Error

SQL_GET = '''
SELECT *
FROM UserPingCount
WHERE userID = ?
'''

SQL_REGISTER = '''
INSERT INTO UserPingCount(userID, numPings)
VALUES(?,?)
'''

SQL_UPDATE = '''
UPDATE UserPingCount
SET numPings = ?
WHERE userID = ?
'''

SQL_DELETE = '''
DELETE
FROM UserPingCount
WHERE userID = ?
'''


def check_for_user(conn, userid):
    cur = conn.cursor()
    cur.execute(SQL_GET, (userid,))
    record = cur.fetchone()
    conn.commit()
    if record is None:
        return False
    else:
        return True


def register_user(conn, userid):
    cur = conn.cursor()
    try:
        cur.execute(SQL_REGISTER, (userid, 1))
    except Error as e:
        print(e)
    conn.commit()


def update_user(conn, userid, new_count):
    cur = conn.cursor()
    cur.execute(SQL_UPDATE, (new_count, userid))
    conn.commit()


def get(conn, userid):
    cur = conn.cursor()
    cur.execute(SQL_GET, (userid,))
    ping_total = cur.fetchone()['numPings']
    conn.commit()
    return ping_total


def clear_user(conn, userid):
    cur = conn.cursor()
    cur.execute(SQL_DELETE, (userid,))
    conn.commit()


def connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(e)

    return conn
