import asyncio
import discord
from discord.ext import commands
import random, logging
import datetime as dt
from yt_api import get_yt_url, get_song_name
from technical import cog_log
import yt_dlp as youtube_dl


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


    @commands.command(name="music")
    @discord.app_commands.checks.has_role(ROLE_ID)
    async def music(self, ctx, url):
        title = get_song_name(url)
        self.title = title
        try:
            try:
                voice_client = await ctx.message.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except discord.errors.ClientException:
                voice_client = voice_clients[ctx.message.guild.id]
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, executable="ffmpeg/bin/ffmpeg.exe", **ffmpeg_options)
            try:
                voice_client.play(player)
            except discord.errors.ClientException:
                voice_clients[ctx.message.guild.id].pause()
                voice_client.play(player)
            await ctx.send(f'Сейчас играет: "{self.title}"')
        except AttributeError:
            await ctx.send(f"{ctx.author.mention}, сначала зайди в голосовой канал")

    @commands.command(name="stop")
    @discord.app_commands.checks.has_role(ROLE_ID)
    async def stop(self, ctx):
        try:
            voice_clients[ctx.message.guild.id].stop()
            await ctx.send(f'Воспроизведение "{self.title}" выключено')
        except Exception:
            await ctx.send("Выключать нечего!")

    @commands.command(name="pause")
    @discord.app_commands.checks.has_role(ROLE_ID)
    async def pause(self, ctx):
        try:
            voice_clients[ctx.message.guild.id].pause()
            await ctx.send(f'Воспроизведение "{self.title}" приостановлено')
        except Exception:
            await ctx.send("Останавливать нечего!")

    @commands.command(name="resume")
    @discord.app_commands.checks.has_role(ROLE_ID)
    async def resume(self, ctx):
        try:
            voice_clients[ctx.message.guild.id].resume()
            await ctx.send(f'Воспроизведение "{self.title}" продолжено')
        except Exception:
            await ctx.send("Трек не остановлен!")


async def setup(bot):
    await bot.add_cog(DevUsers(bot))
    cog_log(bot, __name__)