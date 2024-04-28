import datetime as dt
import logging
from technical import TOKEN
import discord
from discord.ext import commands
import os
import asyncio
import sys
from discord import app_commands
import technical
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


@bot.tree.command(name='test', description="XDDD")
async def test(interaction: discord.Interaction):
    schedule = technical.Schedule()
    schedule_list.append(schedule)
    await interaction.response.send_modal(schedule)


@discord.app_commands.checks.has_role(technical.ROLE_ID)
@bot.tree.command(name='планерка', description="Создание формы планерки")
async def schedule_creation(interaction: discord.Interaction):
    schedule = technical.Schedule()
    schedule_list.append(schedule)
    await interaction.response.send_modal(schedule)


@discord.app_commands.checks.has_role(technical.ROLE_ID)
@bot.tree.command(name='id', description="Имя пользователя по айди")
async def id_name(ctx, id):
    dm = await bot.create_dm(ctx.author)
    await dm.send(bot.get_user(id))




async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start(TOKEN)


asyncio.run(main())
sys.stdout.close()
