import discord
import os
import json

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


@client.event
async def on_ready():
    print("Ready")


for f_name in os.listdir('commands'):
    if f_name.endswith('.py'):
        client.load_extension(f'commands.{f_name[:-3]}')

client.run(TOKEN)
