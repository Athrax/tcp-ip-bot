from typing import Optional

import discord
import requests
from discord.ext import commands
from discord import app_commands
from cogs.message_handler import MessageHandler
from config.config import set_debug_mode
from personality.personality import load_personalities, Personality


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.BotIntegration = bot
        self.current_personality: Optional[Personality] = None
        self.synced = None

    @commands.Cog.listener()
    async def on_ready(self):
        # Synchronisation de l'arbre à commande
        self.synced = await self.bot.tree.sync()
        print(f'[MAIN] Commandes synchronisées ({len(self.synced)})')

    @app_commands.command(name="poweroff", description="Désactiver le bot")
    async def poweroff(self, ctx: discord.Interaction):
        print("[COMMANDE] Commande poweroff reçue")
        await ctx.response.send_message(content="Le bot est désactivé.", ephemeral=True)
        MessageHandler.enabled = False

    @app_commands.command(name="poweron", description="Activer le bot")
    async def poweron(self, ctx: discord.Interaction):
        print("[COMMANDE] Commande poweron reçue")
        await ctx.response.send_message(content="Le bot est activé.", ephemeral=True)
        MessageHandler.enabled = True

    @app_commands.command(name="personality", description="Modifier la personnalité du bot")
    @app_commands.choices(
        personality=[
            app_commands.Choice(name=personality.name, value=personality.name)
            for personality in load_personalities()
        ]
    )
    async def personality(self, interaction: discord.Interaction, personality: str):
        print(f"[COMMANDE] Commande personality reçue : personality={personality}")
        await interaction.response.defer()
        try:
            selected_personality = next((p for p in load_personalities() if p.name == personality), None)
            if selected_personality:
                avatar = requests.get(selected_personality.avatar).content
                await self.bot.user.edit(avatar=avatar)
                await self.bot.user.edit(username=selected_personality.name.capitalize())
                await interaction.followup.send(
                    content=f"La personnalité du bot a été modifiée : [\n{selected_personality.description[:100]}...]",
                    ephemeral=True
                )
                self.current_personality = selected_personality
            else:
                await interaction.followup.send(
                    content="Personnalité non trouvée.", ephemeral=True
                )
        except Exception as e:
            from cogs import llm_api
            print(f"[COMMANDE] Erreur : {e}")
            await interaction.followup.send(
                content="Ohla cowboy, pas trop vite ! Je ne peux pas encore changer de personnalité. Re-essaye un peu "
                        "plus tard !", ephemeral=True
            )

    @app_commands.command(name="debug", description="Activer le mode debug")
    async def debug(self, ctx: discord.Interaction, mode: bool):
        print("[COMMANDE] Commande debug reçue")
        await ctx.response.send_message(content=f"Le mode debug est {'activé.' if mode else 'désactivé.'}",
                                        ephemeral=True)
        print(f"[DEBUG] Mode debug {'activé' if mode else 'désactivé'}")
        set_debug_mode(mode)


async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))
