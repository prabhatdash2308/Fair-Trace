import hashlib
import tiktoken
from typing import Dict, Any
from app.ai.agents.performance.schemas import CostMetrics

# Approximate pricing per 1K tokens for various models (mock values for demonstration)
PRICING = {
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "text-embedding-3-small": {"input": 0.00002, "output": 0.0},
}

def calculate_cost(model: str, usage: Dict[str, int]) -> CostMetrics:
    """Calculates LLM execution costs based on token usage."""
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    cached_tokens = usage.get("cached_tokens", 0) # Mock handling for cached tokens
    total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)
    
    rates = PRICING.get(model, {"input": 0.0, "output": 0.0})
    
    # Calculate input/output cost (discount cached tokens if supported)
    # simplified logic:
    billable_input = prompt_tokens - (cached_tokens * 0.5) # Example mock discount
    if billable_input < 0: billable_input = 0
    
    cost_input = (billable_input / 1000.0) * rates["input"]
    cost_output = (completion_tokens / 1000.0) * rates["output"]
    total_cost = cost_input + cost_output
    
    return CostMetrics(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cached_tokens=cached_tokens,
        total_tokens=total_tokens,
        cost_input=round(cost_input, 6),
        cost_output=round(cost_output, 6),
        total_cost=round(total_cost, 6)
    )

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
