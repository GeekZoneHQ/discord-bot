import discord

from discord.ext import commands


def to_do(ctx):
    ctx.send("pog")


class Job(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Job imported")

    @commands.command()
    async def job_schedule(self, ctx, *arg):
        if not len(arg):
            await ctx.send("no args")
            return

        if len(arg) == 1:
            schedule.every(5).minutes.do(to_do(ctx))


def setup(client):
    client.add_cog(Job(client))
