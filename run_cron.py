#!/usr/bin/env python3
"""Cron launcher for Daily Paper — invokes ollama claude to run the daily papers script."""
import subprocess, sys, os
from datetime import datetime

BASE_DIR = "/Users/xinzhang/daily_paper"
os.environ["PATH"] = "/usr/local/bin:/Users/xinzhang/.local/bin:/opt/homebrew/bin:" + os.environ.get("PATH", "")
CLAUDE_CMD = ["/usr/local/bin/ollama", "launch", "claude", "--model", "kimi-k2.6:cloud", "--"]

prompt = "Run the daily paper script: cd /Users/xinzhang/daily_paper && git switch main && git pull && source venv/bin/activate && python daily_papers.py"

os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

print(f"[{datetime.now().isoformat()}] Starting Daily Paper")
sys.stdout.flush()

result = subprocess.run(
    CLAUDE_CMD + [
        "--print", "-p", prompt,
        "--max-turns", "20",
        "--dangerously-skip-permissions",
    ],
    cwd=BASE_DIR,
    timeout=3600,
)

print(f"[{datetime.now().isoformat()}] Done (exit code {result.returncode})")
sys.exit(result.returncode)
