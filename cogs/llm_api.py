from discord.ext import commands
from typing_extensions import Optional
from personality.personality import Personality, load_personalities

from api.prediction import llm_ask


class LlmApi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[LLM] Chargement de l'API du LLM ...")
        # Vérifier si l'API du LLM fonctionne
        self.init_request()

    def init_request(self):
        try:
            response, time = llm_ask()
        except Exception as e:
            print("[LLM] Erreur : La chargement de l'API du LLM a échoué\n"
                  f"[LLM] Erreur : {e}")
            exit()

        if response:
            print(f"[LLM] L'API a répondu au test : {response}\n"
                  f"[LLM] Latence de l'API : {time} secondes")
        else:
            print(f"[LLM] Erreur : L'API n'a pas répondu au test")


async def setup(bot: commands.Bot):
    await bot.add_cog(LlmApi(bot))
