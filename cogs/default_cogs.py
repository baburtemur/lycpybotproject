import asyncio
import discord
from discord.ext import commands
import random, logging
import datetime as dt

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']


class RandomThings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll _dice')
    async def roll_dice(self, ctx, count):
        res = [random.choice(dashes) for _ in range(int(count))]
        await ctx.send(" ".join(res))

    @commands.command(name='randint')
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith('!'):
            return
        if "привет" in message.content.lower():
            reply = "И тебе привет"
        else:
            reply = "курица гриль"

        await message.channel.send(reply)

        print(
            f'{dt.datetime.now().strftime("%Y-%m-%d %H:%M")} {self.bot.user} ответил "{reply}" на сообщение "{message.content}" '
            f' от @{message.author}'
        )





async def setup(bot):
    await bot.add_cog(RandomThings(bot))