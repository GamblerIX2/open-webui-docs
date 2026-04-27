#!/usr/bin/env python3
"""Run all Chinese localization helper scripts in a stable order."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "translate_auth1.py",
    "translate_batch.py",
    "translate_calendar_notes.py",
    "translate_db2.py",
    "translate_db3.py",
    "translate_db4.py",
    "translate_env.py",
    "translate_files.py",
    "translate_otel.py",
    "translate_plugin.py",
    "translate_plugin_index.py",
    "translate_rag.py",
    "translate_rbac.py",
    "translate_sso.py",
    "translate_terminals.py",
    "translate_tools_functions.py",
    "translate_workspace1.py",
    "translate_workspace2.py",
]


def main() -> int:
    failures: list[str] = []
    for script_name in SCRIPTS:
        script_path = SCRIPT_DIR / script_name
        print(f"=== {script_name} ===")
        result = subprocess.run([sys.executable, str(script_path)], cwd=SCRIPT_DIR.parent)
        if result.returncode != 0:
            failures.append(script_name)

    if failures:
        print("\nFAILED:")
        for name in failures:
            print(f"- {name}")
        return 1

    print("\nAll localization scripts completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
