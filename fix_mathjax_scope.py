#!/usr/bin/env python3
"""
Script to update MathJax configuration to only process takeaways section
"""

import os
import re
from pathlib import Path


def fix_mathjax_scope(file_path):
    """Update MathJax config to disable auto-processing"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already fixed
    if 'Disable automatic processing' in content or 'only for takeaways section' in content:
        return False  # Already fixed

    original_content = content

    # Find and replace the MathJax configuration
    old_config_pattern = r'''    <!-- MathJax for LaTeX rendering -->\s*
    <script>\s*
        MathJax = \{\s*
            tex: \{\s*
                inlineMath: \[\['\$', '\$'\], \['\\\\?\(', '\\\\?\)'\]\],\s*
                displayMath: \[\['\$\$', '\$\$'\], \['\\\\?\[', '\\\\?\]'\]\],\s*
                processEscapes: true,\s*
                processEnvironments: true\s*
            \},\s*
            options: \{\s*
                skipHtmlTags: \['script', 'noscript', 'style', 'textarea', 'pre'\]\s*
            \}\s*
        \};\s*
    </script>'''

    new_config = '''    <!-- MathJax for LaTeX rendering (only for takeaways section) -->
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
            },
            startup: {
                pageReady: () => {
                    // Disable automatic processing - we'll only process takeaways manually
                    return Promise.resolve();
                }
            }
        };
    </script>'''

    content = re.sub(old_config_pattern, new_config, content, flags=re.DOTALL)

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
    print("Fixing MathJax scope to takeaways only...\n")

    fixed_count = 0
    skipped_count = 0

    for html_file in sorted(html_files):
        try:
            if fix_mathjax_scope(html_file):
                print(f"✓ Fixed: {html_file.name}")
                fixed_count += 1
            else:
                print(f"- Skipped (already fixed): {html_file.name}")
                skipped_count += 1
        except Exception as e:
            print(f"✗ Error processing {html_file.name}: {e}")

    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Fixed: {fixed_count} files")
    print(f"  Skipped: {skipped_count} files")
    print(f"  Total: {len(html_files)} files")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
