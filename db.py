import sqlite3
import json

with open('./config.json') as f:
    config = json.load(f)
f.close()


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
            response_id INTEGER,
            bot_message_id INTEGER,
            user_id INTEGER,
            datetime DATETIME,
            FOREIGN KEY (bot_message_id)
                REFERENCES bot_message (bot_message_id),
            FOREIGN KEY (response_id)
                REFERENCES user_response (response_id),
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
    try:
        sql = ("INSERT INTO bot_message (bot_message_id, text) VALUES (?, ?)")
        cursor.execute(sql, (1, config['msg1']))
        cursor.execute(sql, (2, config['msg2']))
        cursor.execute(sql, (3, config['msg3']))
        print("Messages written to DB")
    except sqlite3.IntegrityError:
        sql = ('''UPDATE bot_message
                  SET text = ?
                  WHERE bot_message_id = ?''')
        cursor.execute(sql, (config['msg1'], 1))
        cursor.execute(sql, (config['msg2'], 2))
        cursor.execute(sql, (config['msg3'], 3))
        print("Messages overwritten in DB")
    db.commit()
