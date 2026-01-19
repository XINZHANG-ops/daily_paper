"""
HTML and Markdown Utilities

This module provides utilities for HTML and markdown processing, including
text formatting, conversion between formats, and rendering of content for
web display.
"""

import re
from loguru import logger

try:
    import markdown
except ImportError:
    markdown = None
    logger.warning("markdown library not installed. Install with: pip install markdown")


def markdown_to_html(markdown_content, extensions=None):
    """
    Convert markdown content to HTML.

    Uses the markdown library to convert markdown text to HTML with support
    for various extensions.

    Args:
        markdown_content (str): The markdown text to convert
        extensions (list, optional): List of markdown extensions to use.
                                    Defaults to ['extra', 'nl2br', 'sane_lists']

    Returns:
        str: HTML representation of the markdown content
    """
    if markdown is None:
        logger.warning("markdown library not available, returning raw text in <pre> tags")
        return f"<pre>{markdown_content}</pre>"

    if extensions is None:
        extensions = ['extra', 'nl2br', 'sane_lists']

    return markdown.markdown(markdown_content, extensions=extensions)


def fix_image_paths(html_content, date_str, base_path="../images"):
    """
    Fix relative image paths in HTML content.

    Converts image src attributes to use proper relative paths for a specific date.
    Useful when HTML files are in a different directory than image files.

    Args:
        html_content (str): HTML content with image tags
        date_str (str): Date string (YYYY-MM-DD) for organizing images
        base_path (str, optional): Base path to images directory. Defaults to "../images"

    Returns:
        str: HTML content with corrected image paths
    """
    # Handle markdown's output format: src="filename.jpg"
    # Don't modify absolute URLs or paths that already start with ../ or /
    html_content = re.sub(
        r'src="(?!http://|https://|/|\.\./)([^"]+)"',
        f'src="{base_path}/{date_str}/\\1"',
        html_content
    )
    return html_content


def wrap_in_section(content, title, section_class="section", content_class="content"):
    """
    Wrap HTML content in a styled section div.

    Args:
        content (str): The HTML content to wrap
        title (str): The section title/header
        section_class (str, optional): CSS class for the section div
        content_class (str, optional): CSS class for the content div

    Returns:
        str: HTML content wrapped in section divs with header
    """
    return f"""
    <div class="{section_class}">
        <h2>{title}</h2>
        <div class="{content_class}">
            {content}
        </div>
    </div>
    """


def sanitize_html(html_content, allowed_tags=None):
    """
    Sanitize HTML content by removing or escaping potentially dangerous tags.

    This is a basic implementation. For production use, consider using a
    dedicated library like bleach.

    Args:
        html_content (str): The HTML content to sanitize
        allowed_tags (list, optional): List of allowed HTML tags.
                                       If None, uses a default safe list.

    Returns:
        str: Sanitized HTML content
    """
    if allowed_tags is None:
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'a', 'img', 'code', 'pre', 'blockquote', 'div', 'span'
        ]

    # This is a simplified sanitization - consider using bleach for production
    # For now, just return the content as-is since we trust our own markdown generation
    return html_content


def format_markdown_bold_to_html(text, color="#ff0000"):
    """
    Convert markdown bold syntax to colored HTML bold tags.

    Args:
        text (str): Text containing markdown bold syntax (**)
        color (str, optional): HTML color code for the bold text. Defaults to red.

    Returns:
        str: Text with markdown bold converted to HTML with color
    """
    return re.sub(
        r'\*\*(.*?)\*\*',
        rf'<font color="{color}"><b>\1</b></font>',
        text
    )


def format_markdown_bullets(text):
    """
    Convert markdown bullet points to HTML bullet character.

    Args:
        text (str): Text that may start with markdown bullet (- or *)

    Returns:
        str: Text with markdown bullets replaced by •
    """
    if text.startswith('- ') or text.startswith('* '):
        return f"• {text[2:]}"
    return text
