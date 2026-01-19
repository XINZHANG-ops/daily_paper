"""
HTML template loading utilities.

Provides functions to load and render HTML templates with variable substitution.
"""
import os
from string import Template
from pathlib import Path


# Get the templates directory path
TEMPLATE_DIR = Path(__file__).parent.parent / 'templates'


def load_template(template_name):
    """
    Load an HTML template file.

    Args:
        template_name: Name of the template file (e.g., 'index_template.html')

    Returns:
        str: Template content

    Raises:
        FileNotFoundError: If template file doesn't exist
    """
    template_path = TEMPLATE_DIR / template_name

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def render_template(template_name, **kwargs):
    """
    Load and render a template with variable substitution.

    Args:
        template_name: Name of the template file
        **kwargs: Variables to substitute in the template

    Returns:
        str: Rendered HTML content

    Example:
        >>> html = render_template('index_template.html',
        ...                        date_structure='<div>...</div>',
        ...                        stats='10 papers')
    """
    template_content = load_template(template_name)
    template = Template(template_content)
    return template.substitute(**kwargs)


def get_index_template():
    """
    Get the index page template.

    Returns:
        Template: String Template object for index page
    """
    content = load_template('index_template.html')
    return Template(content)


def get_subpage_template():
    """
    Get the subpage template.

    Returns:
        Template: String Template object for daily paper subpage
    """
    content = load_template('subpage_template.html')
    return Template(content)
