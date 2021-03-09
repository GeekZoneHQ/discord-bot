import discord
import os
import json

import asyncio
import datetime as dt

from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle

load_dotenv()
TOKEN = os.environ.get("TOKEN")

with open('./config.json') as f:
    config = json.load(f)
f.close()
PREFIX = config["prefix"]

client = commands.Bot(PREFIX)
status = cycle(['Status 1', 'Status 2'])


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


def get_task_start(task):
    start_datetime = dt.datetime.strptime(
        config[task]["start"], '%Y-%m-%d %H:%M:%S')
    return start_datetime


def get_task_interval(task):
    pass


get_task_interval("msg1")


@tasks.loop(seconds=5)
async def message1():
    conf = config["msg1"]
    await client.get_channel(conf["channel"]).send(conf["message"])


@message1.before_loop
async def before():
    start_time = get_task_start("msg1")
    for _ in range(60*60*24*7):
        if dt.datetime.now() >= start_time:
            print('It is time')
            print(dt.datetime.now())
            return
        await asyncio.sleep(1)
    await client.wait_until_ready()


@client.event
async def on_ready():
    print("Ready")
    message1.start()


for f_name in os.listdir('commands'):
    if f_name.endswith('.py'):
        client.load_extension(f'commands.{f_name[:-3]}')

client.run(TOKEN)
