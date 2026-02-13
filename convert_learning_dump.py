import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
nb_path = ROOT / "personal" / "LEARNING_DUMP.ipynb"
out_path = nb_path.with_suffix(".md")

nb = json.loads(nb_path.read_text(encoding="utf-8"))

parts: list[str] = []
for cell in nb.get("cells", []):
    ctype = cell.get("cell_type", "")
    src = "".join(cell.get("source", []))
    if ctype == "markdown":
        parts.append(src)
    elif ctype == "code":
        parts.append(f"```python\n{src}\n```")
    else:
        parts.append(src)

out_path.write_text("\n\n".join(parts), encoding="utf-8")
print("Wrote:", out_path)