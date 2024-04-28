import discord
from discord import app_commands
from discord.ext import commands

from technical import cog_log
from yt_api import get_yt_url

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
tree = app_commands.CommandTree(discord.Client(intents=intents))


class DefaultUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="youtube", with_app_command=True, description="Поиск видео в ютубе по запросу")
    async def youtube(self, ctx, request, _id=0):
        await ctx.send(get_yt_url(request, _id))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        dmchannel = await self.bot.create_dm(member)
        await dmchannel.send('Добро пожаловать на наш дискорд канал!')
        await member.guild.system_channel.send(embed=discord.Embed(colour=discord.Colour.dark_embed(),
                                                                   description=f"{member}, привет!"))


async def setup(bot):
    await bot.add_cog(DefaultUsers(bot))
    cog_log(bot, __name__)
