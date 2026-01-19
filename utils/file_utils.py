"""
File I/O Utilities

This module provides functions for file operations including reading paper lists,
loading daily takeaways, and fetching data from external APIs. It handles file
reading, filtering, and data processing tasks.
"""

import os
import re
import requests
from loguru import logger

try:
    import markdown
except ImportError:
    markdown = None
    logger.warning("markdown library not installed. Install with: pip install markdown")


BASE_URL = "https://api.quotable.io"


def find_not_proposed_papers(
        grab_papers: list[dict],
        current_paper_list: list[str],
    ) -> tuple[list[dict], list[str]]:
    """
    Filter out papers that have already been proposed.

    Compares a list of new papers against an existing list of paper titles
    to identify papers that haven't been proposed yet.

    Args:
        grab_papers (list[dict]): List of paper dictionaries with 'title' keys
        current_paper_list (list[str]): List of already proposed paper titles

    Returns:
        tuple: A tuple containing:
            - list[dict]: New papers not in the current list
            - list[str]: Updated list of all paper titles (current + new)
    """
    new_papers = []
    new_titles = []
    for paper_data in grab_papers:
        paper_title = paper_data['title']
        if paper_title in current_paper_list:
            continue
        else:
            new_papers.append(paper_data)
            new_titles.append(paper_title)
    return new_papers, current_paper_list + new_titles


def load_daily_takeaways(date_str):
    """
    Load personal takeaways from markdown file for a specific date.

    Reads a markdown file containing daily notes/takeaways and converts it to HTML.
    Handles image path resolution and styling for the output.

    Args:
        date_str (str): Date in format YYYY-MM-DD

    Returns:
        str: HTML content of the takeaways, or empty string if no file exists
    """
    takeaway_file = f'dailies/notes/{date_str}.md'

    if not os.path.exists(takeaway_file):
        logger.debug(f"No takeaway file found for {date_str}")
        return ""

    try:
        with open(takeaway_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        if not markdown_content.strip():
            return ""

        # Convert markdown to HTML
        if markdown is None:
            logger.warning("markdown library not available, returning raw text")
            # Fallback: wrap in <pre> tags if markdown not available
            return f"<pre>{markdown_content}</pre>"

        # Convert markdown to HTML with extensions for better formatting
        html_content = markdown.markdown(
            markdown_content,
            extensions=['extra', 'nl2br', 'sane_lists']
        )

        # Fix image paths to use relative paths
        # Since HTML is in dailies/pages/, images are in dailies/images/
        # Relative path from pages/ to images/ is ../images/
        # Handle markdown's output format: src="filename.jpg"
        html_content = re.sub(
            r'src="(?!http://|https://|/|\.\./)([^"]+)"',
            f'src="../images/{date_str}/\\1"',
            html_content
        )

        # Wrap in styled divs
        wrapped_html = f"""
    <div class="takeaways-section">
        <h2>📝 My Takeaways</h2>
        <div class="takeaways-content">
            {html_content}
        </div>
    </div>
        """

        logger.debug(f"Loaded takeaways for {date_str}")
        return wrapped_html

    except Exception as e:
        logger.error(f"Error loading takeaways for {date_str}: {e}")
        return ""


def fetch_data(endpoint, params=None):
    """
    Fetch data from the quotable.io API.

    Makes HTTP GET requests to the quotable API to retrieve quotes and related data.
    SSL verification is disabled for compatibility.

    Args:
        endpoint (str): The API endpoint path (e.g., '/random')
        params (dict, optional): Query parameters for the request

    Returns:
        dict: JSON response from the API, or None if request fails
    """
    url = f"{BASE_URL}{endpoint}"
    try:
        # Disable SSL verification
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
