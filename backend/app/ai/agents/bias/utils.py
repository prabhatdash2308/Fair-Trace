import hashlib
import tiktoken

def generate_prompt_hash(system_prompt: str, developer_prompt: str) -> str:
    """Generates a SHA256 hash representing the prompt snapshot."""
    combined = f"{system_prompt}|{developer_prompt}"
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()

def estimate_tokens(text: str, model: str = "gpt-4o") -> int:
    """Estimates the number of tokens in a string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
