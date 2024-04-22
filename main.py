import datetime as dt
import discord
from discord.ext import commands
import logging, random

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = "MTIzMTM0MjgzMzk2NTczMTkyMg.G8yRvV.HVb_qr_EfC5GzyE9GR1LicN36fHczxRE7z3J-A"

dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']


class RandomThings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll_dice')
    async def roll_dice(self, ctx, count):
        res = [random.choice(dashes) for _ in range(int(count))]
        await ctx.send(" ".join(res))

    @commands.command(name='randint')
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)


class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if "привет" in message.content.lower():
            reply = "И тебе привет"
        else:
            reply = "курица гриль"

        await message.channel.send(reply)

        print(
        f'{dt.datetime.now().strftime("%Y-%m-%d %H:%M")} {self.user} ответил "{reply}" на сообщение "{message.content}"'
        f' от @{message.author}'
        )


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='#!', intents=intents)
bot.add_cog(RandomThings(bot))
bot.start(TOKEN)
client = YLBotClient(intents=intents)
client.run(TOKEN)