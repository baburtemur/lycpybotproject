import datetime as dt
import logging
from technical import TOKEN
import discord
from discord.ext import commands
import os
import asyncio
import sys
import shutil

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


class YLBotClient(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')




bot = YLBotClient(command_prefix='!', intents=intents)


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start(TOKEN)


asyncio.run(main())
sys.stdout.close()
