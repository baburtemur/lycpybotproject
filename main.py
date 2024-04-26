import datetime as dt
import logging
from technical import TOKEN
import discord
from discord.ext import commands
import os
import asyncio
import sys
from discord import app_commands
from technical import Schedule, DiscordEvents
from discord.abc import Snowflake, Object


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
fh = logging.FileHandler("logs/logs.txt")
fh.setLevel(logging.ERROR)
logger.addHandler(fh)
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.presences = True


class YLBotClient(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def setup_hook(self):
        bot.tree.copy_global_to(guild=discord.Object(id=1231344759487070249))
        await bot.tree.sync(guild=discord.Object(id=1231344759487070249))

        print(f"commands for {self.user} are ready!")


bot = YLBotClient(command_prefix='!', intents=intents)
schedule_list = []
_queue = asyncio.Queue()

@bot.tree.command(name='test', description="XDDD")
async def test(interaction: discord.Interaction):
    schedule = Schedule()
    schedule_list.append(schedule)
    await interaction.response.send_modal(schedule)


@bot.tree.command(name='abc', description="XDDD")
async def test(interaction: discord.Interaction):
    schedule = Schedule()
    schedule_list.append(schedule)
    await interaction.response.send_modal(schedule)


@bot.event
async def on_reaction_add(reaction, user):
    if len(schedule_list) > 0:
        for schedule in schedule_list:
            if schedule.message.id == reaction.message.id:
                pass#schedule.add

@bot.event
async def on_scheduled_event_create(event):
    await _queue.put(event.url)
    print(event.url)
    print(123412314123412314123412314123412314123412314123412314123412314123412314123412314123412314123412314123412314)




async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start(TOKEN)


asyncio.run(main())
sys.stdout.close()
