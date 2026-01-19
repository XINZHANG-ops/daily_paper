"""
HuggingFace API integration utilities.

Functions for fetching and processing papers from HuggingFace Daily Papers.
"""
import requests
from datetime import datetime, timezone
from loguru import logger


def fetch_huggingface_papers(limit=100):
    """
    Fetches papers from the Hugging Face API endpoint.

    Args:
        limit: Maximum number of papers to fetch

    Returns:
        list: Raw paper data from HuggingFace API
    """
    API_URL = "https://huggingface.co/api/daily_papers"

    try:
        response = requests.get(f"{API_URL}?limit={limit}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching papers: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []


def process_papers(papers, sort_method="hot"):
    """
    Process and sort the papers based on the specified method.

    Args:
        papers: Raw paper data from HuggingFace API
        sort_method: Sorting algorithm - "hot", "rising", or "new"

    Returns:
        list: Processed and sorted papers with metadata
    """
    processed_papers = []

    for paper in papers:
        title = paper.get('title', 'No title')
        paper_id = paper.get('paper', {}).get('id', '')
        url = f"https://huggingface.co/papers/{paper_id}"
        authors = [author.get('name', '') for author in paper.get('paper', {}).get('authors', [])]
        upvotes = paper.get('paper', {}).get('upvotes', 0)
        comments = paper.get('numComments', 0)
        published_at_str = paper.get('publishedAt', datetime.now(timezone.utc).isoformat())

        try:
            published_time = datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
        except ValueError:
            published_time = datetime.now(timezone.utc)

        time_diff = datetime.now(timezone.utc) - published_time
        days_ago = time_diff.days

        if sort_method == "hot":
            time_diff_hours = time_diff.total_seconds() / 3600
            score = upvotes / ((time_diff_hours + 2) ** 1.5)
        elif sort_method == "rising":
            time_diff_hours = time_diff.total_seconds() / 3600
            score = upvotes / (time_diff_hours + 1)
        else:  # "new" - just use published time
            score = published_time.timestamp()

        processed_papers.append({
            'title': title,
            'url': url,
            'paper_id': paper_id,
            'authors': authors,
            'upvotes': upvotes,
            'comments': comments,
            'published_at': published_time.isoformat(),
            'days_ago': days_ago,
            'score': score
        })

    if sort_method == "new":
        return sorted(processed_papers, key=lambda x: x['published_at'], reverse=True)
    else:  # "hot" or "rising"
        return sorted(processed_papers, key=lambda x: x['score'], reverse=True)


def get_huggingface_papers(sort_method="hot", limit=100):
    """
    Main function to fetch and process HuggingFace papers.

    Args:
        sort_method: Sorting algorithm - "hot", "rising", or "new"
        limit: Maximum number of papers to fetch

    Returns:
        list: Processed and sorted papers
    """
    raw_papers = fetch_huggingface_papers(limit)
    if raw_papers:
        return process_papers(raw_papers, sort_method)
    return []
