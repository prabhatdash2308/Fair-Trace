import os
from pathlib import Path

# Update builder.py
builder_file = Path("backend/app/ai/graph/builder.py")
b_content = builder_file.read_text(encoding="utf-8")
b_content = b_content.replace('"explainability", self.nodes.explainability_node', '"explainability_step", self.nodes.explainability_node')
b_content = b_content.replace('add_conditional_edges("explainability",', 'add_conditional_edges("explainability_step",')
b_content = b_content.replace('"explainability": "explainability",', '"explainability_step": "explainability_step",')
builder_file.write_text(b_content, encoding="utf-8")

# Update edges.py
edges_file = Path("backend/app/ai/graph/edges.py")
e_content = edges_file.read_text(encoding="utf-8")
e_content = e_content.replace('return default_router(state, "explainability")', 'return default_router(state, "explainability_step")')
e_content = e_content.replace('def route_after_explainability(state: ReviewState) -> str:', 'def route_after_explainability_step(state: ReviewState) -> str:')
edges_file.write_text(e_content, encoding="utf-8")

# Let's ensure builder.py calls edges.route_after_explainability_step
b_content = builder_file.read_text(encoding="utf-8")
b_content = b_content.replace('edges.route_after_explainability', 'edges.route_after_explainability_step')
builder_file.write_text(b_content, encoding="utf-8")

print("Fixed node name conflicts.")
