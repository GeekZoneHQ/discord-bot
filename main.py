import discord
import os
import json

import asyncio
import datetime as dt

from discord.ext import commands, tasks
from dotenv import load_dotenv
from db import create_db

load_dotenv()
TOKEN = os.environ.get("TOKEN")

with open('./config.json') as f:
    config = json.load(f)
f.close()
PREFIX = config["prefix"]

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=PREFIX, intents=intents)


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
        config["start"], '%Y-%m-%d %H:%M:%S')
    return start_datetime


def get_task_interval():
    interval_d, interval_t = config["interval"].split(" ")
    hours, minutes, seconds = interval_t.split(":")
    hours = hours + interval_d * 24
    return int(hours), int(minutes), int(seconds)


@tasks.loop()
async def message1():
    guild = client.get_guild(config["guild"])
    role = guild.get_role(config["role"])
    for user in guild.members:
        if role in user.roles:
            await user.send(config["msg1"])

            def is_pog(m):
                return (m.author == user
                        and isinstance(m.channel, discord.channel.DMChannel))

            try:
                guess = await client.wait_for(
                    'message', check=is_pog, timeout=9.0
                )
            except asyncio.TimeoutError:
                return await user.send("9 seconds have passed")

            if guess:
                await user.send(guess.content)


@message1.before_loop
async def before():
    start_time = get_task_start()
    for _ in range(60*60*24*7):
        if dt.datetime.now() >= start_time:
            print('It is time')
            hours, minutes, seconds = get_task_interval()
            message1.change_interval(
                hours=hours,
                minutes=minutes,
                seconds=seconds)
            return
        await asyncio.sleep(1)
    await client.wait_until_ready()


@client.event
async def on_ready():
    print("Initialzing database")
    create_db()
    print("Database initialzed")
    print("Ready")
    message1.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return


for f_name in os.listdir('commands'):
    if f_name.endswith('.py'):
        client.load_extension(f'commands.{f_name[:-3]}')

client.run(TOKEN)
