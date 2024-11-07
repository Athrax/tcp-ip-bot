from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands
from cogs.message_handler import MessageHandler
from config.config import set_debug_mode
from personality.personality import load_personalities


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.BotIntegration = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

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
        selected_personality = next((p for p in load_personalities() if p.name == personality), None)
        if selected_personality:
            print(f"[COMMANDE] Commande personality reçue : {selected_personality.name}")
            await interaction.response.send_message(
                content=f"La personnalité du bot a été modifiée : [\n{selected_personality.description}]",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                content="Personnalité non trouvée.", ephemeral=True
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
