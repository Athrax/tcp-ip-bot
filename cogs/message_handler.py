import discord
from discord.ext import commands

from config.config import LLM_MUTED_CHANNELS, LLM_IGNORED_MEMBERS
from debug.debug import debug


class MessageHandler(commands.Cog):
    enabled = True

    def __init__(self, bot):
        self.bot: discord.BotIntegration = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        author_dn: str = message.author.display_name
        channel_id: int = message.channel.id

        # Ignorer les messages du bot
        if message.author.id is self.bot.user.id:
            debug(f"[LLM] Abandon de la réponse : message envoyé par le bot")
            return

        # Vérification des permissions
        if not check_permissions(message=message):
            debug(f"[LLM] Abandon de la réponse à {author_dn} sur le canal {channel_id}")
            return

        # Traitement du message


async def setup(bot: commands.Bot):
    await bot.add_cog(MessageHandler(bot))


def check_permissions(message: discord.Message):
    def check_permit_channel() -> bool:
        return message.channel.id in LLM_MUTED_CHANNELS

    def check_permit_member() -> bool:
        return message.author.id in LLM_IGNORED_MEMBERS

    # Verifier les permissions
    return check_permit_channel() and check_permit_member()
