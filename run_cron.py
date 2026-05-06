#!/usr/bin/env python3
"""Cron launcher for Daily Paper — runs daily_papers.py directly."""
import subprocess, sys, os
from datetime import datetime

BASE_DIR = "/Users/xinzhang/daily_paper"
VENV_PYTHON = os.path.join(BASE_DIR, "venv", "bin", "python")
os.environ["PATH"] = "/usr/local/bin:/Users/xinzhang/.local/bin:/opt/homebrew/bin:" + os.environ.get("PATH", "")

os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

print(f"[{datetime.now().isoformat()}] Starting Daily Paper")
sys.stdout.flush()

subprocess.run(["git", "switch", "main"], cwd=BASE_DIR)
subprocess.run(["git", "pull"], cwd=BASE_DIR)

result = subprocess.run(
    [VENV_PYTHON, "daily_papers.py"],
    cwd=BASE_DIR,
    timeout=3600,
)

print(f"[{datetime.now().isoformat()}] Done (exit code {result.returncode})")
sys.exit(result.returncode)
