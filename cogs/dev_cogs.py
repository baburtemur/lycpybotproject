import asyncio
import discord
from discord.ext import commands
from async_timeout import timeout
import technical
from technical import cog_log, ROLE_ID, TIME_MUTE
import yt_dlp as youtube_dl
from data.__all_models import add_user
import datetime as dt

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
    @commands.command("warn")
    async def warn(self, ctx):
        if ctx.message.type == discord.MessageType.reply:
            reference = await ctx.fetch_message(ctx.message.reference.message_id)
            member = reference.author
            status = add_user(member.id)
            if status == 3:
                await ctx.send.message(f"Прощай {member}!")
                await self.bot.kick(member)
            if status == 2:
                try:
                    ff = discord.utils.utcnow() + dt.timedelta(seconds=TIME_MUTE)
                    await member.edit(timed_out_until=ff)
                    await ctx.send(f"{member} отправлен в тайм-аут до {str(ff)[:-13]}")
                except discord.errors.Forbidden:
                    await ctx.send(f"У вас не хватает прав!")

    @discord.app_commands.checks.has_role(ROLE_ID)
    @discord.app_commands.command(name="settings")
    async def settings(self, ctx):
        dm = await self.bot.create_dm(ctx.author)
        if ctx.author.has_permissions(administrator=True):
            await dm.send("Направляю список настроек")
            async with ctx.typing():
                await asyncio.sleep(2.5)
                mes = ""
                dt = technical.SETTINGS
                for elem in list(dt.keys()):
                    mes += f"{elem} = {dt[elem]}"
                await dm.send(mes)
                await dm.send("Чтобы изменить любой параметр ответьте на это сообщение по форме:\nПАРАМЕТР=НовоеЗначение")
                def check(m, user):
                    return user.id == ctx.author.id and
                await self.bot.wait_for("message", check=check, timeout=300)

        else:
            await dm.send('')





async def setup(bot):
    await bot.add_cog(DevUsers(bot))
    cog_log(bot, __name__)