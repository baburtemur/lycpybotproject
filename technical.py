import sys, inspect
import discord
from discord import ui, app_commands
import datetime as dt
import calendar

TOKEN = "MTIzMTM0MjgzMzk2NTczMTkyMg.G8yRvV.HVb_qr_EfC5GzyE9GR1LicN36fHczxRE7z3J-A"
YT_API = "AIzaSyDq4ROZColssRSxsQl1Rpt0weyrAb7uMrw"


def cog_log(bot, name):
    clsmembers = inspect.getmembers(sys.modules[name], inspect.isclass)
    for elem in clsmembers:
        try:
            if type(elem[0]) is str:
                cog = bot.get_cog(str(elem[0]))
                command = cog.get_commands()
                print(f"{elem[0]}_commands:{[c.name for c in command]}")
        except AttributeError:
            pass


class Schedule(ui.Modal, title='Форма планерки'):
    text = ui.TextInput(label='На повестке дня:', style=discord.TextStyle.paragraph, max_length=300)
    mon = ui.TextInput(label="Месяц", placeholder=f"{dt.date.today().month}", style=discord.TextStyle.short,
                       max_length=10, required=True)
    day = ui.TextInput(label="День", placeholder=f"{dt.date.today().day}", style=discord.TextStyle.short,
                       max_length=2, required=True)
    time = ui.TextInput(label="Начало", placeholder=f"{dt.datetime.now().hour + 4}:{dt.datetime.now().strftime('%M')}",
                       style=discord.TextStyle.short, max_length=5, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        author = interaction.user
        mention = author.mention
        embed = discord.Embed(color=discord.Color.dark_blue(), title="Назначение встречи",
                              description=f"{mention} назначил встречу на "
                                          f"{calendar.month_name[int(str(self.mon))]}, {str(self.day)}, "
                                          f"в {str(self.time)}\n**Цель встречи**:\n{str(self.text)}\n")
        embed.add_field(name="Чтобы обозначить своё участие",
                        value="используйте любую реакцию под этим сообщением", inline=False)
        allowed_mentions = discord.AllowedMentions(everyone=True)
        embed.set_author(name=author.name, icon_url=author.avatar)
        ff = await interaction.response.send_message('@everyone', embed=embed,
                                                allowed_mentions=allowed_mentions)
        print(ff.id)
        await ff.add_reaction('\N{THUMBS UP SIGN}')


# for member in discord.Interaction.guild.members:
# Schedule.members.append_option(discord.SelectOption(label=member.name, description=member.role))
# members = ui.Select(placeholder="Выберете участников планерки", min_values=0, max_values=1, options=[d
# iscord.SelectOption(label='Никого')])
# type=discord.ComponentType.user_select
