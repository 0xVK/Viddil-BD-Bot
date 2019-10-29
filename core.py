import settings
import sqlite3
import os
import datetime


def create_user_stats_table_if_not_exists():

    query = """CREATE TABLE IF NOT EXISTS user_statistics(
                  request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  telegram_id TEXT,
                  username TEXT,
                  full_name TEXT,
                  activity TEXT,
                  point INTEGER,
                  datetime TEXT DEFAULT (datetime('now', 'localtime')))"""

    return DBManager.execute_query(query)


def add_points(u_id, username, full_name, activity, points):

    query = """INSERT INTO user_statistics (
          telegram_id,
          username,
          full_name,
          activity,
          point) VALUES (?, ?, ?, ?, ?)"""

    return DBManager.execute_query(query, (u_id, username, full_name, activity, points))


def get_user_stat_by_id(t_id):

    query = """SELECT * FROM user_statistics where telegram_id = ?"""

    res = DBManager.execute_query(query, (t_id,))

    s = ''

    if not res:
        return 'Пусто'

    for row in res:
        s += '<b>{}</b>: {} ({})\n' .format(row[4], row[6], row[5])

    return s


def get_ranking():

    query = """SELECT full_name, sum(point) as 'count'
    FROM user_statistics
    GROUP BY telegram_id
    ORDER BY sum(point) DESC"""

    resp = DBManager.execute_query(query)

    if not resp:
        return 'Пусто'

    s = ''

    for row in resp:
        s += '<b>{}</b>: {}\n'.format(row[0], row[1])

    return s


class DBManager:

    @classmethod
    def execute_query(cls, query, *args):  # returns result or true if success, or false when something go wrong

        try:
            connection = sqlite3.connect(os.path.join(settings.BASE_DIR, settings.DATABASE), check_same_thread=False)

            cursor = connection.cursor()
            cursor.execute(query, *args)
            connection.commit()
            query_result = cursor.fetchall()
            cursor.close()
            connection.close()

            if query_result:
                return query_result
            return False

        except sqlite3.Error as ex:

            log(m='Query error: {}'.format(str(ex)))
            return -1


def log(chat=None, m=''):

    now_time = datetime.datetime.now().strftime('%d-%m %H:%M:%S')

    with open(os.path.join(settings.BASE_DIR, 'bot_log.txt'), 'a', encoding="utf-8") as log_file:
        if chat:
            log_file.write('[{}]: ({} {}) {}\n'.format(now_time, chat.first_name, chat.last_name, m))
        else:
            log_file.write('[{}]: (Server) {}\n'.format(now_time, m))

