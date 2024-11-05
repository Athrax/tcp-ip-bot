import asyncio
import os

import discord  # nom du package à installer : discord.py, et non discord
from discord.ext import commands

from config.config import DEFAULT_TOKEN_FILE_PATH
from config.token import token_loader

# Intialisation des intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Intialisation du bot
bot = commands.Bot(command_prefix='!', intents=intents)


# Charger les modules
async def load():
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'[MODULE] Chargement du module {filename[:-3]}')


# Fonction principale
async def main():
    print("[MAIN] Chargment du bot ...")
    # Charger les modules
    await load()
    # Lancer le bot
    while True:
        try:
            await bot.start(token_loader(DEFAULT_TOKEN_FILE_PATH))
        except Exception as e:
            raise e
            print(f"[MAIN] Erreur : {e}")
            await asyncio.sleep(3)


if __name__ == '__main__':
    asyncio.run(main())
