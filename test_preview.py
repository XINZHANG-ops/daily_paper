#!/usr/bin/env python3
"""Test the markdown preview rendering"""

import re

def render_markdown_preview(md_text, date=None, uploaded_images=None):
    """Convert markdown to HTML with proper LaTeX support"""
    if not md_text:
        return "<p style='color: #888;'>Start typing to see preview...</p>"

    # Fix image paths if date is provided
    if date:
        # Replace image references to point to the correct location
        md_text = re.sub(
            r'!\[([^\]]*)\]\((?!http://|https://|/)([^)]+)\)',
            f'![\\1](dailies/images/{date}/\\2)',
            md_text
        )

    # Step 1: Protect LaTeX blocks from markdown processing
    latex_blocks = {}
    placeholder_counter = [0]

    def store_latex(match):
        placeholder = f"___LATEX_BLOCK_{placeholder_counter[0]}___"
        latex_blocks[placeholder] = match.group(0)
        placeholder_counter[0] += 1
        return placeholder

    # Protect display math $$...$$
    html_text = re.sub(r'\$\$[\s\S]*?\$\$', store_latex, md_text)
    # Protect inline math $...$
    html_text = re.sub(r'\$[^\$\n]+?\$', store_latex, html_text)

    # Step 2: Process markdown to HTML
    # Headers
    html_text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html_text, flags=re.MULTILINE)
    html_text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html_text, flags=re.MULTILINE)
    html_text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html_text, flags=re.MULTILINE)

    # Bold (now safe since LaTeX is protected)
    html_text = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', html_text)

    # Italic
    html_text = re.sub(r'\*([^*\n]+?)\*', r'<em>\1</em>', html_text)

    # Links (process before images to avoid conflicts)
    html_text = re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', html_text)

    # Images
    html_text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" style="max-width: 100%; height: auto;">', html_text)

    # Step 3: Restore LaTeX blocks
    for placeholder, latex in latex_blocks.items():
        html_text = html_text.replace(placeholder, latex)

    # Step 4: Format paragraphs and line breaks
    lines = html_text.split('\n')
    result_lines = []
    current_paragraph = []

    for line in lines:
        stripped = line.strip()
        if stripped == '':
            if current_paragraph:
                para_text = '<br>'.join(current_paragraph)
                if not (para_text.startswith('<h') or para_text.startswith('$$')):
                    para_text = f'<p>{para_text}</p>'
                result_lines.append(para_text)
                current_paragraph = []
        else:
            current_paragraph.append(stripped)

    if current_paragraph:
        para_text = '<br>'.join(current_paragraph)
        if not (para_text.startswith('<h') or para_text.startswith('$$')):
            para_text = f'<p>{para_text}</p>'
        result_lines.append(para_text)

    html_text = '\n'.join(result_lines)
    return html_text


# Test cases
print("=" * 60)
print("Test 1 - Bold text:")
test_text_1 = "This is **bold text** and this is normal text"
result1 = render_markdown_preview(test_text_1)
print(result1)
print()

print("=" * 60)
print("Test 2 - Inline LaTeX with spaces:")
test_text_2 = "$Citation-aware Group Relative Policy Optimization (C-GRPO)$"
result2 = render_markdown_preview(test_text_2)
print(result2)
print()

print("=" * 60)
print("Test 3 - Full markdown with LaTeX:")
test_text_3 = """# For paper **Learnable Multipliers**

The paper discussed a quite deep problem. This is **bold** text.

$$
\|W\| \\approx \sqrt{\\frac{\eta}{\lambda}}
$$

And some more text with $inline math$ here."""

result3 = render_markdown_preview(test_text_3)
print(result3)
print()

print("=" * 60)
print("Test 4 - Complex case with bold AND LaTeX:")
test_text_4 = "The **multipliers** are defined as $s_i$ where **s** is learnable."
result4 = render_markdown_preview(test_text_4)
print(result4)
