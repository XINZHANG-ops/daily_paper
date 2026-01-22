"""
Simple launcher script for the Paper Selection UI
Run this file to start the Gradio interface
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

TEST = os.getenv("TEST")

print("""
╔══════════════════════════════════════════════╗
║      Daily Papers Selection UI Starting      ║
╚══════════════════════════════════════════════╝

Configuration:
- TEST Mode: {}
- Server: http://localhost:7860

Press Ctrl+C to stop the server
""".format(os.environ['TEST']))

try:
    from pick_paper_ui import create_ui
    ui = create_ui()
    ui.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
        theme="soft"
    )
except Exception as e:
    print(f"Error starting UI: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")