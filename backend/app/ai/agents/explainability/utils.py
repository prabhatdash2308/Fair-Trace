import hashlib
import tiktoken

def generate_prompt_hash(system_prompt: str, developer_prompt: str) -> str:
    combined = f"{system_prompt}|{developer_prompt}"
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()

def estimate_tokens(text: str, model: str = "gpt-4o") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
