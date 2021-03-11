import sqlite3


def create_db():
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_message (
            bot_message_id INTEGER NOT NULL PRIMARY KEY,
            text TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER NOT NULL PRIMARY KEY
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_message_sent (
            bot_message_sent_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_message_id INTEGER,
            user_id INTEGER,
            datetime DATETIME,
            FOREIGN KEY (bot_message_id)
                REFERENCES bot_message (bot_message_id),
            FOREIGN KEY (user_id)
                REFERENCES user (user_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_response (
            response_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT,
            datetime DATETIME,
            FOREIGN KEY (user_id)
                REFERENCES user (user_id)
        )
    ''')
