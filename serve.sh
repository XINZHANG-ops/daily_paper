#!/bin/bash
# Simple HTTP server to view daily papers locally
# This avoids CORS issues with file:// protocol

echo "Starting local server..."
echo "Open your browser to: http://localhost:8000/dailies/pages/2026-01-02.html"
echo "Press Ctrl+C to stop the server"
python3 -m http.server 8000
