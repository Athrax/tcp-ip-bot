import discord
from discord.ext import commands


class MyClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(MyClass(bot))