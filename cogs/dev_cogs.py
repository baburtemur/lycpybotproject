import asyncio
import discord
from discord.ext import commands
from data.__all_models import add_accession
import technical
from technical import cog_log, ROLE_ID, TIME_MUTE
import yt_dlp as youtube_dl
from data.__all_models import add_user
import datetime as dt
from schedule import Schedule

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
    @commands.hybrid_command("warn", with_app_command=True, description="Выдать предупреждение")
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
    @discord.app_commands.command(name="git", description="Ссылка на Гит")
    async def git(self, interaction):
        add_accession(interaction.user.id, dt.datetime.now(dt.timezone.utc))
        requester = interaction.user
        dm = await self.bot.create_dm(requester)
        if technical.GIT_ACCESSIONS_LOG:
            log = self.bot.get_user(technical.GIT_ACCESSIONS_LOG)
            log_dm = await self.bot.create_dm(log)

            await log_dm.send(f"""{dt.datetime.now(dt.timezone.utc)}: {requester.name}
             из сервера {interaction.guild.name} вошёл в ваш Гит\n\nЧтобы отключить уведомления вызовите 
             /settings и поставьте у параметра GIT_ACCESSIONS_LOG=None""", silent=True)

        await dm.send(f"{requester.mention}\n\nСсылка на Гит: "
                      f"{technical.GIT_LINK}, держите её в секрете!", delete_after=60)
        await interaction.response.send_message("Гит отправлен", ephemeral=True)

    @discord.app_commands.checks.has_role(ROLE_ID)
    @discord.app_commands.command(name="settings", description="Настройки Бота")
    async def settings(self, interaction):
        dm = await self.bot.create_dm(interaction.user)
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Права подтверждены", ephemeral=True)
            async with dm.typing():
                await asyncio.sleep(2.5)
                embed = discord.Embed(color=discord.Colour.dark_blue(), title="Список настроек")
                header = "ПАРАМЕТРЫ:"
                mes = ""
                dt = technical.SETTINGS
                for elem in list(dt.keys()):
                    mes += f"{elem} = {dt[elem]}\n"
                embed.add_field(name=header, value=mes)
                embed.set_footer(
                    text=
                    "Чтобы изменить любой параметр ответьте на это сообщение по форме:\n\nПАРАМЕТР=значение\n\n"
                    "Перечисляйте параметры через пробел"
                )
                await dm.send(embed=embed, silent=True)

            def check(m):
                print(m)
                return m.author.id == interaction.user.id and isinstance(m.channel, discord.DMChannel)

            reply = await self.bot.wait_for("message", check=check, timeout=300)
            async with dm.typing():
                try:
                    technical.parser(str(reply.content).strip())
                    await dm.send("Параметры обновленны!")
                except Exception as e:
                    print(e)
                    await dm.send("Некорректный ввод, правильная форма: ПАРАМЕТР=значение")
        else:
            await interaction.response.send_message("Права не подтверждены", ephemeral=True)

    @discord.app_commands.checks.has_role(technical.ROLE_ID)
    @discord.app_commands.command(name='schedule', description="Создание формы планерки")
    async def schedule_creation(self, interaction: discord.Interaction):
        schedule = Schedule()
        await interaction.response.send_modal(schedule)

    @discord.app_commands.checks.has_role(technical.ROLE_ID)
    @discord.app_commands.command(name='id', description="Имя пользователя по айди")
    async def id_name(self, ctx, _id: int):
        dm = await self.bot.create_dm(ctx.author)
        await dm.send(self.bot.get_user(_id))


async def setup(bot):
    await bot.add_cog(DevUsers(bot))
    cog_log(bot, __name__)
