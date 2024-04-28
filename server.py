import logging
import os
import sys
import asyncio
import discord
from discord.ext import commands
from technical import TOKEN

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
bot.remove_command('help')


async def load():
    bot.get_command('schedule')
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start(TOKEN)


asyncio.run(main())
sys.stdout.close()
