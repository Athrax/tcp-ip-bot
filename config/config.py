# Paramètre général
DEBUG_MODE: bool = False

# Paramètre LLM
HUGGING_FACE_CLIENT_ID: str = "yuntian-deng/ChatGPT4"
LLM_NUCLEUS_SMAPLING: float = 1
LLM_TEMPERATURE: float = 1

# Paramètres de chemin de fichiers
DEFAULT_TOKEN_FILE_PATH: str = "config/token.txt"
DEFAULT_PERSONALITIES_FILE_PATH: str = "config/personalities.json"
DEFAULT_CONTEXTS_FILE_PATH: str = "config/contexts.json"

# Paramètres de messages
LLM_MUTED_CHANNELS = [

]
LLM_IGNORED_MEMBERS = [

]

# Base de donnée
DATABASE_FILE = "data/database.sql"

# Modification des paramètres de debug
def set_debug_mode(mode: bool) -> None:
    global DEBUG_MODE
    DEBUG_MODE = mode
