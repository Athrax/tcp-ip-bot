BASE_PROMPT: str = """<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
{}
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
{}<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>"""

DEFAULT_SYSTEM_PROMPT = """Tu es un bot discord, cette requête permet de tester si l'API fonctionne."""
DEFAULT_USER_PROMPT = """Salut, est-ce que tu es opérationnel ?"""
