import os
from pathlib import Path

# Fix nodes.py
nodes_file = Path("backend/app/ai/graph/nodes.py")
content = nodes_file.read_text(encoding="utf-8")
content = content.replace("PipelineStatus.IN_PROGRESS", "PipelineStatus.RUNNING")
nodes_file.write_text(content, encoding="utf-8")

# Fix test
test_file = Path("tests/ai/test_langgraph.py")
test_content = test_file.read_text(encoding="utf-8")
test_content = test_content.replace("PipelineStatus.IN_PROGRESS", "PipelineStatus.RUNNING")
test_file.write_text(test_content, encoding="utf-8")

print("Fixed IN_PROGRESS -> RUNNING")
