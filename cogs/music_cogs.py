import asyncio

import discord
import yt_dlp as youtube_dl
from discord.ext import commands
from discord.utils import get
from async_timeout import timeout
from technical import cog_log
from yt_api import get_song_name

ROLE_ID = 1232060135908835348
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
voice_clients = {}
yt_dl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
LIMIT = 15


class YtSource(discord.PCMVolumeTransformer):
    def __init__(self, source, url, requester, volume=0.5):
        super().__init__(source, volume=volume)
        self.requester = requester
        self.title = get_song_name(url)
        self.url = url

    @classmethod
    async def create_source(cls, data, url, loop=None):
        loop = loop or asyncio.get_event_loop()
        requester = data.message.author
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, executable="ffmpeg/bin/ffmpeg.exe", **ffmpeg_options), url=url,
                   requester=requester, volume=0.5)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self._await = asyncio.Queue()
        self.next = asyncio.Event()
        self.quembed = discord.Embed(color=discord.Color.dark_red(), description="Все треки в очереди:",
                                     title="Очередь треков")

    async def quembed_ini(self, ctx, status="Выключено"):
        embed = self.quembed.copy()
        vc = ctx.voice_client
        if vc.is_paused():
            status = "Пауза"
        if vc.is_playing():
            status = "Играет"
        fields = []
        for elem in list(self.queue):
            fields.append((elem.title, elem.url, False))
        fields.append(('Статус', status, True))
        fields.append(('Сейчас играет:', self.queue[0].title, True))
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        return embed

    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(f"{ctx.message.author.mention}, зайди в голосовой канал!")
            return
        else:
            await ctx.send(f'Захожу в канал `{ctx.message.author.voice.channel}`')
        await ctx.message.author.voice.channel.connect()

    @commands.command("music", with_app_command=True, description="Начать воспроизведение музыки")
    async def music(self, ctx, url):
        await self.add_queue(ctx, url)
        ctx.bot.loop.create_task(self.music_loop(ctx))

    async def music_loop(self, ctx):
        await self.bot.wait_until_ready()
        try:
            async with timeout(300):
                player = await self._await.get()
                if self.next.is_set():
                    self.next.clear()
        except asyncio.TimeoutError:
            await ctx.send('Время ожидания истекло! улетучиваюсь')
            await self.leave(ctx)
        await self.music_cleanup(ctx, player=player)
        await self.next.wait()
        self.queue.pop(0)
        ctx.bot.loop.create_task(self.music_loop(ctx))

    async def music_cleanup(self, ctx, player):
        await ctx.send(f"Играет {player.title}, запрошенное {ctx.message.author.mention}")
        await self.start_playing(ctx, ctx.voice_client)
        await self.next.wait()
        if len(self.queue) == 0:
            await ctx.send("Воспроизведение закончено")
            await self.leave(ctx)

    async def start_playing(self, ctx, voice_client):
        embed = await self.quembed_ini(ctx, status="Играет")
        await ctx.send(embed=embed)
        try:
            voice_client.play(self.queue[0], after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
        except Exception as e:
            print(e.upper())
            await ctx.send("Возникла непредвиденная ошибка!")

    @commands.hybrid_command("add_queue", with_app_command=True, description="Добавляет трек в конец очереди")
    async def add_queue(self, ctx, url):
        if len(self.queue) == LIMIT:
            await ctx.send(f"Очередь заполнена")
            return
        player = await YtSource.create_source(ctx, url, loop=self.bot.loop)
        self.queue.append(player)

        await self._await.put(player)

    @commands.hybrid_command("remove_queue", with_app_command=True, description="Убирает трек в конце очереди")
    async def remove_queue(self, ctx, number):
        try:
            self.queue.pop(number)
        except IndexError:
            ctx.send(f"{ctx.message.author.mention}, в списке всего {len(self.queue)}!")
        if len(self.queue) < 1:
            await ctx.send("Очередь пуста")
        else:
            await ctx.send(f'Ваша очередь {len(self.queue)}/{LIMIT} теперь выглядит так:\n')
            embed = await self.quembed_ini(ctx)
            await ctx.send(embed=embed)

    @commands.hybrid_command("pause", with_app_command=True, description="Приостановить воспроизведение")
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.pause()
        user = ctx.message.author.mention
        await ctx.send(f"Воспроизведение приостановлено {user}")

    @commands.hybrid_command("resume", with_app_command=True, description="Продолжить воспроизведение")
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.resume()
        user = ctx.message.author.mention
        await ctx.send(f"Воспроизведение продолжено {user}")

    @commands.hybrid_command("clear_queue", with_app_command=True, description="Очистить очередь")
    async def clear_queue(self, ctx):
        self.queue.clear()
        user = ctx.message.author.mention
        await ctx.send(f"Очередь очищенна {user}")

    @commands.hybrid_command("view_queue", with_app_command=True, description="Показать очередь")
    async def view_queue(self, ctx):
        if len(self.queue) < 1:
            await ctx.send('Очередь пока что пуста - используйте /add_queue [ссылка] или !add_queue "ссылка"')
        else:
            await ctx.send(f'Ваша очередь {len(self.queue)}/{LIMIT} теперь выглядит так:')
            embed = await self.quembed_ini(ctx)
            await ctx.send(embed=embed)

    @classmethod
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        user = ctx.message.author.mention
        await voice_client.disconnect()
        await ctx.send(f'Disconnected from {user}')

    @music.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(f"{ctx.author.mention}, сначала зайди в голосовой канал")
                return
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


async def setup(bot):
    await bot.add_cog(Music(bot))
    cog_log(bot, __name__)
