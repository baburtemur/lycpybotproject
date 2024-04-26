import asyncio
import discord
from discord.ext import commands
import random, logging
import datetime as dt
from yt_api import get_yt_url, get_song_name
from technical import cog_log
import yt_dlp as youtube_dl
from typing import Union

ROLE_ID = 1232060135908835348
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
voice_clients = {}
yt_dl_opts = {'format': 'bestaudio'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


class DevUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.title = "тут ничего не проигрывается"

    @discord.app_commands.checks.has_role(ROLE_ID)
    @commands.hybrid_command("schedule")
    async def schedule(self, ctx, date: str, channel: Union[str]):
        if isinstance(channel, str):
            pass



async def setup(bot):
    await bot.add_cog(DevUsers(bot))
    cog_log(bot, __name__)