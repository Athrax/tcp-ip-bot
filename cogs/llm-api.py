from discord.ext import commands

from api.prediction import llm_ask


class LlmApi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[LLM] Chargement de l'API du LLM ...")
        self.init_request()

    def init_request(self):
        try:
            response, time = llm_ask()
        except Exception as e:
            print("[LLM] Erreur : La chargement de l'API du LLM a échoué")
            print(f"[LLM] Erreur : {e}")
            exit()

        if response:
            print(f"[LLM] L'API a répondu au test : {response}")
            print(f"[LLM] Latence de l'API : {time} secondes")
        else:
            print(f"[LLM] Erreur : L'API n'a pas répondu au test")


async def setup(bot: commands.Bot):
    await bot.add_cog(LlmApi(bot))
