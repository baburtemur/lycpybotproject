from re import A
import technical
import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def run():
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        for server in bot.guilds:
            await bot.tree.sync(guild=discord.Object(id=server.id))

    @bot.tree.command(name='mur', description="Welcomes user", nsfw=True)
    async def ciao(interaction: discord.Interaction):
        await interaction.response.send_message(f"Ciao! {interaction.user.mention}")

    bot.run(technical.TOKEN, root_logger=True)


if __name__ == "__main__":
    run()