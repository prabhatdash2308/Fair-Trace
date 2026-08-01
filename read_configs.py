import os
files = [
    "backend/app/ai/services/llm/config.py",
    "backend/app/ai/services/embeddings/config.py",
    "backend/app/ai/services/vector_store/config.py"
]
for f in files:
    print(f"--- {f} ---")
    with open(f, "r") as file:
        print(file.read())
