import discord
from discord.ext import commands
from technical import cog_log


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", with_app_command=True, description="Вывод всех комманд бота")
    async def send_bot_help(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple(), title="Список команд")
        for name in self.bot.cogs:
            cog = self.bot.get_cog(name)
            cog_desc = ""
            for command in cog.get_commands():
                cog_desc += f'{command.name} - {command.description}\n'
            for command in cog.get_app_commands():
                cog_desc += f'{command.name} - {command.description}\n'
            embed.add_field(name=name, value=cog_desc, inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
    cog_log(bot, __name__)
