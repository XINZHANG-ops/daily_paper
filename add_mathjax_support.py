#!/usr/bin/env python3
"""
Script to add MathJax support to all HTML files in dailies/pages/
"""

import os
import re
from pathlib import Path


def add_mathjax_to_html(file_path):
    """Add MathJax support to a single HTML file"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if MathJax is already added
    if 'MathJax' in content or 'mathjax' in content:
        return False  # Already has MathJax

    original_content = content

    # 1. Add MathJax configuration and script right after marked.js
    mathjax_code = '''
    <!-- MathJax for LaTeX rendering -->
    <script>
        MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true,
                processEnvironments: true
            },
            options: {
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            }
        };
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

'''

    # Insert MathJax after marked.js
    marked_pattern = r'(<script src="https://cdn\.jsdelivr\.net/npm/marked/marked\.min\.js"></script>)\s*\n(\s*<script>)'
    marked_replacement = r'\1' + mathjax_code + r'\2'
    content = re.sub(marked_pattern, marked_replacement, content)

    # 2. Add MathJax typeset call after inserting takeaways content
    typeset_code = '''
                            // Trigger MathJax to render LaTeX equations
                            if (typeof MathJax !== 'undefined') {
                                MathJax.typesetPromise([document.getElementById('takeaways-container')])
                                    .then(() => {
                                        console.log('MathJax rendering complete');
                                    })
                                    .catch((err) => console.error('MathJax rendering error:', err));
                            }'''

    # Insert after the takeaways rendering
    render_pattern = r"(document\.getElementById\('takeaways-container'\)\.innerHTML = wrappedHtml;\s*console\.log\('Takeaways section rendered'\);)"
    render_replacement = r"\1" + typeset_code
    content = re.sub(render_pattern, render_replacement, content)

    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    """Process all HTML files in dailies/pages/"""
    pages_dir = Path('dailies/pages')

    if not pages_dir.exists():
        print(f"Error: {pages_dir} directory not found!")
        return

    html_files = list(pages_dir.glob('*.html'))

    if not html_files:
        print(f"No HTML files found in {pages_dir}")
        return

    print(f"Found {len(html_files)} HTML files in {pages_dir}")
    print("Adding MathJax support...\n")

    fixed_count = 0
    skipped_count = 0

    for html_file in sorted(html_files):
        try:
            if add_mathjax_to_html(html_file):
                print(f"✓ Added MathJax: {html_file.name}")
                fixed_count += 1
            else:
                print(f"- Skipped (already has MathJax): {html_file.name}")
                skipped_count += 1
        except Exception as e:
            print(f"✗ Error processing {html_file.name}: {e}")

    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Added MathJax: {fixed_count} files")
    print(f"  Skipped: {skipped_count} files")
    print(f"  Total: {len(html_files)} files")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
