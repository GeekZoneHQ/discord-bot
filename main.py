import discord
import os
import json

import asyncio
import datetime as dt
import sqlite3

from discord.ext import commands, tasks
from dotenv import load_dotenv
from db import create_db

load_dotenv()
TOKEN = os.environ.get('TOKEN')

with open('./config.json') as f:
    config = json.load(f)
f.close()
PREFIX = config['prefix']

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=PREFIX, intents=intents)

try:
    os.remove('db.sqlite3')
except PermissionError:
    print("DB open")
except FileNotFoundError:
    print("DB does not exist yet")
db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()


@client.command()
async def load(ctx, extension):
    client.load_extension(f'commands.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'commands.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'commands.{extension}')
    client.load_extension(f'commands.{extension}')


def get_task_start():
    start_datetime = dt.datetime.strptime(
        config['start'], '%Y-%m-%d %H:%M:%S')
    return start_datetime


def get_task_interval():
    interval_d, interval_t = config['interval'].split(' ')
    hours, minutes, seconds = interval_t.split(":")
    hours = hours + interval_d * 24
    return int(hours), int(minutes), int(seconds)


@tasks.loop()
async def message():
    guild = client.get_guild(config['guild'])
    role = guild.get_role(config['role'])
    for user in guild.members:
        if role in user.roles:
            sql = (f'''INSERT OR IGNORE INTO user
                       (user_id)
                       VALUES ({user.id})''')
            cursor.execute(sql)
            print(f'Sending first message to: {str(user)}')
            await user.send(config["msg1"])
            sql = ('''INSERT INTO bot_message_sent
                      (bot_message_id, user_id, datetime)
                      VALUES (1, ?, ?)''')
            val = (user.id, dt.datetime.now())
            cursor.execute(sql, val)
            db.commit()


@message.before_loop
async def before():
    start_time = get_task_start()
    for _ in range(60*60*24*7*2):
        if dt.datetime.now() >= start_time:
            hours, minutes, seconds = get_task_interval()
            message.change_interval(
                hours=hours,
                minutes=minutes,
                seconds=seconds)
            return
        await asyncio.sleep(1)
    await client.wait_until_ready()


@client.event
async def on_ready():
    print('Initialzing database')
    create_db()
    print('Database initialzed')
    print('Ready')
    message.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.channel.DMChannel):
        sql = (f'''SELECT * FROM bot_message_sent
                   WHERE user_id = {message.author.id}
                   ORDER BY datetime DESC''')
        cursor.execute(sql)
        try:
            recent = cursor.fetchone()
            if recent[1] is None:
                sql = ('''INSERT INTO user_response
                          (user_id, text, datetime)
                          VALUES (?, ?, ?)''')
                val = (message.author.id, message.content, message.created_at)
                cursor.execute(sql, val)

                sql = ('SELECT MAX(response_id) FROM user_response')
                cursor.execute(sql)
                resp_id = cursor.fetchone()

                sql = ('''UPDATE bot_message_sent
                          SET response_id = ?
                          WHERE bot_message_sent_id = ?''')
                val = (resp_id[0], recent[0])
                cursor.execute(sql, val)
                db.commit()

                if recent[2] == 1:
                    print(f'Sending second message to: {str(message.author)}')
                    await message.author.send(config["msg2"])
                    sql = ('''INSERT INTO bot_message_sent
                              (bot_message_id, user_id, datetime)
                              VALUES (2, ?, ?)''')
                    val = (message.author.id, dt.datetime.now())
                    cursor.execute(sql, val)
                    db.commit()
                elif recent[2] == 2:
                    print(f'Sending third message to: {str(message.author)}')
                    await message.author.send(config["msg3"])
                    sql = ('''INSERT INTO bot_message_sent
                              (bot_message_id, user_id, datetime)
                              VALUES (3, ?, ?)''')
                    val = (message.author.id, dt.datetime.now())
                    cursor.execute(sql, val)
                    db.commit()
                elif recent[2] == 3:
                    print(f'Sending fourth message to: {str(message.author)}')
                    await message.author.send(config["msg4"])
                    sql = ('''INSERT INTO bot_message_sent
                              (bot_message_id, user_id, datetime)
                              VALUES (4, ?, ?)''')
                    val = (message.author.id, dt.datetime.now())
                    cursor.execute(sql, val)
                    db.commit()
                elif recent[2] == 4:
                    print(f'Received all messages from {str(message.author)}')
                    await message.author.send(config["last"])
                    sql = (f'''SELECT text FROM user_response
                               WHERE user_id = {str(message.author.id)}
                               ORDER BY response_id DESC''')
                    cursor.execute(sql)
                    messages = cursor.fetchmany(4)
                    print(messages)
        except TypeError:
            print(f"Not expecting message from {str(message.author)}")


for f_name in os.listdir('commands'):
    if f_name.endswith('.py'):
        client.load_extension(f'commands.{f_name[:-3]}')

client.run(TOKEN)
