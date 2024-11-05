from discord.ext import commands


class MyClass(commands.Cog):  # Nommer la classe par son objectif
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):  # Attribuer des variables lorsque le bot est pret
        pass

    # Corps de cog


async def setup(bot: commands.Bot):
    await bot.add_cog(MyClass(bot))
