import asyncio
import discord
from discord.ext import commands
import random, logging
import datetime as dt
from yt_api import get_yt_url
from technical import cog_log, Schedule
import youtube_dl
from discord import app_commands

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
tree = app_commands.CommandTree(discord.Client(intents=intents))

class DefaultUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="youtube", with_app_command=True, desciption="svo ")
    async def youtube(self, ctx, request, id=0):
        await ctx.send(get_yt_url(request, id))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith('!'):
            return
        if "привет" in message.content.lower():
            reply = "И тебе привет"
        else:
            reply = "курица гриль"

        await message.channel.send(reply)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        dmchannel = await self.bot.create_dm(member)
        await dmchannel.send('Добро пожаловать на наш дискорд канал!')
        await member.guild.system_channel.send(embed=discord.Embed(colour=discord.Colour.dark_embed(),
                                                                   description=f"{member}, привет!"))


async def setup(bot):
    await bot.add_cog(DefaultUsers(bot))
    global tree
    tree = bot.tree
    print(type(bot))
    cog_log(bot, __name__)
