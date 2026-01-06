#!/usr/bin/env python3
"""
Add marked.js script to HTML files that are missing it.
"""

import os
import re
from pathlib import Path
from loguru import logger

def needs_marked_script(html_content):
    """Check if file needs the marked.js script."""
    has_marked_usage = 'marked.parse' in html_content
    has_marked_script = 'marked.min.js' in html_content or 'marked/marked.min.js' in html_content
    return has_marked_usage and not has_marked_script

def add_marked_script(html_content):
    """Add marked.js script before other scripts or before takeaways-container."""
    # Find the takeaways-container div
    container_match = re.search(r'<div id="takeaways-container"></div>', html_content)
    if not container_match:
        return html_content, False

    # Insert the script right before the container
    insert_pos = container_match.start()
    modified_content = (
        html_content[:insert_pos] +
        '    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>\n    ' +
        html_content[insert_pos:]
    )

    return modified_content, True

def process_file(file_path, dry_run=False):
    """Process a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not needs_marked_script(content):
            return False

        modified_content, was_modified = add_marked_script(content)

        if was_modified and not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)

        return was_modified

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function."""
    pages_dir = Path('dailies/pages')
    html_files = sorted(pages_dir.glob('*.html'))

    logger.info(f"Checking {len(html_files)} files...")

    # Dry run
    to_modify = []
    for html_file in html_files:
        if process_file(html_file, dry_run=True):
            to_modify.append(html_file)

    logger.info(f"Found {len(to_modify)} files that need marked.js script")

    if not to_modify:
        logger.success("All files already have marked.js!")
        return

    # Actually modify
    for html_file in to_modify:
        process_file(html_file, dry_run=False)
        logger.success(f"Added marked.js to {html_file.name}")

    logger.success(f"✓ Complete! Added marked.js to {len(to_modify)} files")

if __name__ == "__main__":
    main()
