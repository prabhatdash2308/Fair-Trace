import os
import re

for directory in [
    "backend/app/ai/services/llm",
    "backend/app/ai/services/embeddings",
    "backend/app/ai/services/vector_store",
    "backend/app/ai/prompts"
]:
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "__init__.py":
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                matches = re.finditer(r"def __init__\([^)]+\):", content, re.DOTALL)
                for match in matches:
                    print(f"--- {filepath} ---")
                    print(match.group(0))
