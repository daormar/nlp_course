#!/usr/bin/env python3
"""
fix_kernelspec.py
-----------------
Normalizes the kernelspec of a single notebook (.ipynb) to be compatible
with Google Colab without any kernel warning or error.

Usage:
    python fix_kernelspec.py notebook.ipynb
"""

import json
import sys
from pathlib import Path

COLAB_KERNELSPEC = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}

def fix_notebook(path: Path) -> None:
    if not path.exists():
        print(f"Error: file '{path}' not found.")
        sys.exit(1)

    if path.suffix != ".ipynb":
        print(f"Error: '{path}' is not a .ipynb file.")
        sys.exit(1)

    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Error reading '{path}': {e}")
        sys.exit(1)

    metadata = nb.setdefault("metadata", {})
    current_name = metadata.get("kernelspec", {}).get("name", "(none)")

    if current_name == "python3":
        print(f"'{path.name}' already uses python3. No changes made.")
        return

    metadata["kernelspec"] = COLAB_KERNELSPEC

    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"'{path.name}': '{current_name}' -> 'python3'")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_kernelspec.py notebook.ipynb")
        sys.exit(1)

    fix_notebook(Path(sys.argv[1]))
