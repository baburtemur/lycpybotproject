import asyncio
import discord
from discord.ext import commands
import random, logging
import datetime as dt
from yt_api import get_yt_url
from technical import cog_log
import youtube_dl


intents = discord.Intents.all()
intents.members = True
intents.message_content = True
voice_clients = {}
yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}


class DefaultUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#C:\Users\ProPCUser\PycharmProjects
    @commands.command(name='youtube')`
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

        print(
            f'{dt.datetime.now().strftime("%Y-%m-%d %H:%M")} {self.bot.user} ответил "{reply}" на сообщение "{message.content}" '
            f' от @{message.author}'
        )


async def setup(bot):
    await bot.add_cog(DefaultUsers(bot))
    cog_log(bot, __name__)