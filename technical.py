import sys, inspect
import discord
from discord import ui, app_commands
import datetime as dt
import calendar
import json
import requests
import asyncio
from async_timeout import timeout
TOKEN = "MTIzMTM0MjgzMzk2NTczMTkyMg.G8yRvV.HVb_qr_EfC5GzyE9GR1LicN36fHczxRE7z3J-A"
YT_API = "AIzaSyDq4ROZColssRSxsQl1Rpt0weyrAb7uMrw"
BOT_ID = 1231342833965731922
BOT_AUTH_HEADER = "https://discord.com/oauth2/authorize"

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
    duration = ui.TextInput(label="Длительность", placeholder="02:00",
                       style=discord.TextStyle.short, max_length=5, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        author = interaction.user
        mention = author.mention
        delta = dt.timedelta(hours=-3)
        delta += dt.timedelta(hours=int(str(self.time).split(':')[0]), minutes=int(str(self.time).split(':')[1]))
        time_bef = str(delta)
        time_before = time_bef.split(':')
        delta += dt.timedelta(hours=int(str(self.duration).split(':')[0]), minutes=int(str(self.duration).split(':')[1]))
        time_af = str(delta)
        time_after = time_af.split(':')
        year = dt.datetime.now().year
        if int(str(self.mon)) < dt.datetime.now().month:
            year += 1
        dt_string_s = f"{str(year)}-{str(self.mon)}-{str(self.day)}T{time_before[0]}:{time_before[1]}"
        dt_string_e = f"{str(year)}-{str(self.mon)}-{str(self.day)}T{time_after[0]}:{time_after[1]}"
        event_creator = DiscordEvents()

        url = await event_creator.create_guild_event(
            guild_id= str(interaction.guild_id),
            event_name="Запланированная встреча",
            event_description=f"Встреча запланированная {author}",
            event_start_time=str(dt.datetime.strptime(dt_string_s, "%Y-%m-%dT%H:%M")),
            event_end_time=str(dt.datetime.strptime(dt_string_e, "%Y-%m-%dT%H:%M")),
            event_metadata={'location': 'Developer server'}
        )
        embed = discord.Embed(color=discord.Color.dark_blue(), title="Назначение встречи",
                              description=f"{mention} назначил встречу на "
                                          f"{calendar.month_name[int(str(self.mon))]} {str(self.day)}, "
                                          f"с {time_bef[:-3]} до {time_af[:-3]}\n"
                                          f"**Цель встречи**:\n{str(self.text)}\n")
        embed.add_field(name="Чтобы обозначить своё участие",
                        value=f"перейдите по этой ссылке:\n{url}", inline=False)
        allowed_mentions = discord.AllowedMentions(everyone=True)
        embed.set_author(name=author.name, icon_url=author.avatar)
        await interaction.response.send_message('@everyone', embed=embed,
                                                allowed_mentions=allowed_mentions)
        self.message = await interaction.original_response()


class DiscordEvents:
    def __init__(self) -> None:
        self.base_api_url = 'https://discord.com/api/v9'
        self.auth_headers = {
            "Authorization": f"Bot {TOKEN}",
            "User-Agent": f"DiscordBot ({BOT_AUTH_HEADER}) Python/3.8 aiohttp/3.9.5",
            "Content-Type": "application/json"
        }

    async def create_guild_event(
        self,
        guild_id: str,
        event_name: str,
        event_description: str,
        event_start_time: str,
        event_end_time: str,
        event_metadata: dict,
        event_privacy_level=2,
        channel_id=None
    ) -> str:
        event_create_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        event_data = json.dumps({
            'name': event_name,
            'privacy_level': event_privacy_level,
            'scheduled_start_time': event_start_time,
            'scheduled_end_time': event_end_time,
            'description': event_description,
            'channel_id': channel_id,
            'entity_metadata': event_metadata,
            'entity_type': 3
        })
        response = requests.post(event_create_url, headers=self.auth_headers, data=event_data)
        print(response.status_code, response.text)
        id = json.loads(response.content)['id']
        return "https://discord.com/events/{}/{}".format(guild_id, id)
