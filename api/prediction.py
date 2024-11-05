import time
from gradio_client import Client
from gradio_client.utils import QueueError

from config.config import HUGGING_FACE_CLIENT_ID, LLM_NUCLEUS_SMAPLING, LLM_TEMPERATURE
from config.prompts import BASE_PROMPT, DEFAULT_SYSTEM_PROMPT, DEFAULT_USER_PROMPT
from debug.debug import debug


def llm_ask(system_prompt: str = DEFAULT_SYSTEM_PROMPT, user_prompt: str = DEFAULT_USER_PROMPT) -> tuple[str, float]:
    """
    Interroge le llm avec un prompt système et un prompt d'utilisateur
    :param system_prompt:
    :param user_prompt:
    :return: Retourne la réponse du LLM ainsi que le temps de traitement en seconde
    """
    prompt: str = BASE_PROMPT.format(system_prompt, user_prompt)
    return llm_predict(prompt=prompt)


def llm_predict(prompt: str) -> tuple[str, float]:
    """
    Permet d'interagir avec l'API d'un LLM via un prompt et renvoi sa réponse
    :param prompt: Prompt sur laquelle la prédiction porte
    :return: Retourne la réponse du LLM ainsi que le temps de traitement en seconde
    """

    def api_prediction(prompt_sended: str):
        debug(f"[LLM] Prompt : {prompt_sended}")
        try:
            client: Client = Client(HUGGING_FACE_CLIENT_ID)
            result: str = client.predict(
                inputs=prompt_sended,
                top_p=LLM_NUCLEUS_SMAPLING,
                temperature=LLM_TEMPERATURE,
                chat_counter=0,
                chatbot=[],
                api_name="/predict"
            )
            clean_response: str = result[0][0][1]
            debug(f"[LLM] Réponse : {clean_response}")
            return clean_response
        except QueueError as e:
            print(f"[LLM] Erreur : Impossible d'effectuer la prédiction\n"
                  f"[LLM] Erreur : La requête a été mise en file d'attente, l'API est temporairement indisponible\n"
                  f"[LLM] Erreur : {e}")
            return ""
        except Exception as e:
            print(f"[LLM] Erreur : Impossible d'effectuer la prédiction\n"
                  f"[LLM] Erreur : {e}")
            return ""

    start_time: float = time.time()  # Commence à mesurer le temps
    response: str = api_prediction(prompt)
    end_time: float = time.time()  # Arrête de mesurer le temps
    elapsed_time: float = round(end_time - start_time, 1)
    debug(f"[LLM] L'opération a pris {elapsed_time} secondes.")

    return response, elapsed_time