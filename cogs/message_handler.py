import json
from http.client import responses

import discord
from discord.ext import commands

from config.config import LLM_MUTED_CHANNELS, LLM_IGNORED_MEMBERS, DEFAULT_CONTEXTS_FILE_PATH
from data.connection import execute_query, execute_read_query, archive_message


class MessageHandler(commands.Cog):
    enabled = True

    def __init__(self, bot):
        self.bot: discord.BotIntegration = bot
        self.contexts: dict = json.loads(open('config/contexts.json').read())

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print("[MESSAGE] Message reçu")
        try:
            author_dn: str = message.author.display_name
            author_id: int = message.author.id
            channel_id: int = message.channel.id
            channel_name: str = message.channel.name
            message_id: int = message.id
            content: str = message.content
            bot_id: int = self.bot.user.id

            # Archiver le message
            archive_message(message_id, channel_id, content, author_id)

            # Ignorer les messages du bot
            if author_id is bot_id:
                print(f"[LLM] Abandon de la réponse : message envoyé par le bot")
                return

            # Vérification des permissions
            if check_permissions(message=message):
                print(f"[LLM] Abandon de la réponse à {author_dn} sur le canal {channel_id}")
                return

            # Traitement du message
            print(f"[MESSAGE] #{channel_name} @{author_dn} {content}")
            context = self.contexts[channel_id]
            response: str = message_processing(message, context)

            # Envoyer la réponse
            send_response(response)
        except Exception as e:
            print(f"[MESSAGE] Erreur : {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(MessageHandler(bot))


def check_permissions(message: discord.Message):
    def check_permit_channel() -> bool:
        return message.channel.id in LLM_MUTED_CHANNELS

    def check_permit_member() -> bool:
        return message.author.id in LLM_IGNORED_MEMBERS

    # Verifier les permissions
    return check_permit_channel() or check_permit_member()


def message_processing(message: discord.Message, context: str) -> str:
    # Caractéristique du message
    author: discord.User = message.author
    text: str = message.content
    channel: discord.TextChannel = message.channel

    # Traitement de l'historique
    history = execute_read_query("""SELECT author_id, content FROM history ORDER BY timestamp""")
    print(history)


def get_context(message):
    return ""


def send_response(response):
    print(response)
