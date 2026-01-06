#!/usr/bin/env python3
"""
Script to add takeaway section to existing daily paper HTML files.
Only adds the section if it's missing.
"""

import os
import re
from pathlib import Path
from loguru import logger

def has_takeaway_section(html_content):
    """Check if HTML already has the takeaway container."""
    return 'id="takeaways-container"' in html_content or 'My Takeaways' in html_content

def has_marked_script(html_content):
    """Check if HTML has the marked.js script."""
    return 'marked.min.js' in html_content or 'marked/marked.min.js' in html_content

def add_takeaway_section(html_content):
    """
    Add the takeaway section and necessary scripts if they're missing.

    The takeaway section should be added before the closing </body> tag.
    The marked.js script should be added before the existing scripts.
    """
    # Check what's missing
    needs_container = not has_takeaway_section(html_content)
    needs_script = not has_marked_script(html_content)

    if not needs_container and not needs_script:
        return html_content, False

    modified_content = html_content

    # Add the takeaway container div before </body>
    if needs_container:
        # Find the position before </body> or before the first <script> tag
        script_match = re.search(r'<script', modified_content)
        body_match = re.search(r'</body>', modified_content)

        if script_match:
            insert_pos = script_match.start()
            modified_content = (
                modified_content[:insert_pos] +
                '\n    <!-- Personal Takeaways Section -->\n' +
                '    <div id="takeaways-container"></div>\n\n    ' +
                modified_content[insert_pos:]
            )
        elif body_match:
            insert_pos = body_match.start()
            modified_content = (
                modified_content[:insert_pos] +
                '\n    <!-- Personal Takeaways Section -->\n' +
                '    <div id="takeaways-container"></div>\n\n' +
                modified_content[insert_pos:]
            )

    # Add marked.js script if missing
    if needs_script:
        script_match = re.search(r'<script', modified_content)
        if script_match:
            insert_pos = script_match.start()
            modified_content = (
                modified_content[:insert_pos] +
                '    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>\n    ' +
                modified_content[insert_pos:]
            )

    return modified_content, True

def add_takeaway_styles(html_content):
    """
    Add the CSS styles for takeaway section if they're missing.
    """
    if 'takeaways-section' in html_content:
        return html_content, False

    # Find the closing </style> tag
    style_close = re.search(r'</style>', html_content)
    if not style_close:
        return html_content, False

    takeaway_styles = """
        /* Personal Takeaways Section Styles */
        .takeaways-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 30px;
            margin: 40px 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .takeaways-section h2 {
            color: #ffffff;
            font-size: 2em;
            margin-bottom: 20px;
            border-bottom: 3px solid rgba(255, 255, 255, 0.3);
            padding-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        .takeaways-content {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 8px;
            padding: 25px;
            line-height: 1.8;
            color: #333;
        }

        .takeaways-content h3 {
            color: #667eea;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        .takeaways-content img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 15px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .takeaways-content p {
            margin: 15px 0;
        }

        .takeaways-content ul, .takeaways-content ol {
            margin: 15px 0;
            padding-left: 30px;
        }

        .takeaways-content li {
            margin: 8px 0;
        }

        .takeaways-content blockquote {
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            color: #555;
        }

        .takeaways-content pre {
            background-color: #f6f8fa;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            border: 1px solid #e1e4e8;
        }

        .takeaways-content code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #d73a49;
        }

        .takeaways-content pre code {
            background-color: transparent;
            padding: 0;
            color: #333;
        }
    """

    insert_pos = style_close.start()
    modified_content = (
        html_content[:insert_pos] +
        takeaway_styles + '\n    ' +
        html_content[insert_pos:]
    )

    return modified_content, True

def add_takeaway_script(html_content):
    """
    Add the JavaScript to load markdown takeaways if it's missing.
    """
    if 'Load and render markdown takeaways' in html_content:
        return html_content, False

    # Find existing script tag or position before </body>
    script_match = re.search(r'<script>', html_content)
    body_match = re.search(r'</body>', html_content)

    if not (script_match or body_match):
        return html_content, False

    takeaway_script = """    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Load and render markdown takeaways
            const dateMatch = document.querySelector('h1').textContent.match(/(\\d{4}-\\d{2}-\\d{2})/);
            if (dateMatch) {
                const date = dateMatch[1];
                const markdownPath = `../notes/${date}.md`;

                // Fetch the markdown file
                const xhr = new XMLHttpRequest();
                xhr.open('GET', markdownPath, true);
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        const markdownContent = xhr.responseText;
                        if (!markdownContent.trim()) {
                            console.log('Markdown file is empty');
                            return;
                        }

                        // Convert markdown to HTML
                        let htmlContent = marked.parse(markdownContent);

                        // Fix image paths
                        const fixedContent = htmlContent.replace(
                            /src="(?!http:\\/\\/|https:\\/\\/|\\/|\\.\\.\\/)(.*?)"/g,
                            `src="../images/${date}/$1"`
                        );

                        // Wrap in styled divs
                        const wrappedHtml = `
                            <div class="takeaways-section">
                                <h2>📝 My Takeaways</h2>
                                <div class="takeaways-content">
                                    ${fixedContent}
                                </div>
                            </div>
                        `;

                        document.getElementById('takeaways-container').innerHTML = wrappedHtml;
                        console.log('Takeaways section rendered');
                    } else {
                        console.log('XHR failed - Status:', xhr.status);
                    }
                };
                xhr.onerror = function() {
                    console.log('No takeaway file found for this date');
                };
                xhr.send();
            }
        });
    </script>
"""

    # Insert before </body>
    if body_match:
        insert_pos = body_match.start()
        modified_content = (
            html_content[:insert_pos] +
            takeaway_script + '\n' +
            html_content[insert_pos:]
        )
        return modified_content, True

    return html_content, False

def process_html_file(file_path, dry_run=False):
    """
    Process a single HTML file to add takeaway section if missing.

    Args:
        file_path: Path to the HTML file
        dry_run: If True, only check what would be changed without modifying files

    Returns:
        tuple: (was_modified, changes_made)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes = []

        # Add styles
        content, styles_added = add_takeaway_styles(content)
        if styles_added:
            changes.append("CSS styles")

        # Add container and marked.js
        content, section_added = add_takeaway_section(content)
        if section_added:
            changes.append("takeaway container")

        # Add loading script
        content, script_added = add_takeaway_script(content)
        if script_added:
            changes.append("loading script")

        if content != original_content:
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            return True, changes

        return False, []

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return False, []

def main():
    """Main function to process all HTML files."""
    pages_dir = Path('dailies/pages')

    if not pages_dir.exists():
        logger.error(f"Directory {pages_dir} does not exist!")
        return

    html_files = sorted(pages_dir.glob('*.html'))
    total_files = len(html_files)

    logger.info(f"Found {total_files} HTML files to check")

    # Dry run first
    logger.info("Running dry run to check what would be changed...")
    modified_count = 0
    for html_file in html_files:
        was_modified, changes = process_html_file(html_file, dry_run=True)
        if was_modified:
            modified_count += 1
            logger.info(f"Would modify {html_file.name}: {', '.join(changes)}")

    logger.info(f"\nDry run complete: {modified_count} files would be modified out of {total_files}")

    # Ask for confirmation
    response = input(f"\nProceed with modifying {modified_count} files? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        logger.info("Operation cancelled")
        return

    # Actually modify files
    logger.info("\nProcessing files...")
    modified_count = 0
    for html_file in html_files:
        was_modified, changes = process_html_file(html_file, dry_run=False)
        if was_modified:
            modified_count += 1
            logger.success(f"Modified {html_file.name}: {', '.join(changes)}")

    logger.success(f"\n✓ Complete! Modified {modified_count} out of {total_files} files")

if __name__ == "__main__":
    main()
