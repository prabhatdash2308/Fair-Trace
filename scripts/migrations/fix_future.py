from pathlib import Path

file_path = Path("backend/app/ai/state/review_state.py")
content = file_path.read_text(encoding="utf-8")
content = content.replace("from __future__ import annotations", "")
new_content = "from __future__ import annotations\n" + content
file_path.write_text(new_content, encoding="utf-8")
print("Fixed future imports")
