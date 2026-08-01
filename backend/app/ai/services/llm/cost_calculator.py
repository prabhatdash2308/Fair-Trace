"""
Calculates the estimated USD cost of an LLM request.
"""
class CostCalculator:
    # Example rates per 1k tokens
    RATES = {
        "gpt-4o": {"prompt": 0.005, "completion": 0.015},
        "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.0006},
    }

    @classmethod
    def calculate(cls, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        rate = cls.RATES.get(model, cls.RATES["gpt-4o"])
        prompt_cost = (prompt_tokens / 1000.0) * rate["prompt"]
        completion_cost = (completion_tokens / 1000.0) * rate["completion"]
        return prompt_cost + completion_cost
