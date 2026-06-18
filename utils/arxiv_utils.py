"""
arXiv integration utilities.

Functions for downloading and processing papers from arXiv.
"""
import io
import os
import re
from datetime import date
import requests
from pypdf import PdfReader
from loguru import logger

PDF_CACHE_DIR = os.path.expanduser("~/daily_paper/pdf_cache")


def extract_arxiv_id(paper_info):
    """
    Extract the arXiv ID from paper information.

    Args:
        paper_info: Either a dict with paper_id/url or a string ID

    Returns:
        str: arXiv ID (format: YYMM.number) or None
    """
    if isinstance(paper_info, dict):
        paper_id = paper_info.get('paper_id')
        if not paper_id and 'url' in paper_info:
            url = paper_info['url']
            # Extract ID from URLs like https://huggingface.co/papers/2502.18417
            match = re.search(r'papers/(\d+\.\d+)', url)
            if match:
                paper_id = match.group(1)
    else:
        paper_id = paper_info

    # Verify it looks like an arXiv ID (YYMM.number format)
    if paper_id and re.match(r'\d{4}\.\d+', paper_id):
        return paper_id
    return None


def get_arxiv_pdf_url(paper_info):
    """
    Get the PDF URL for an arXiv paper.

    Args:
        paper_info: Either a dict with paper_id/url or a string ID

    Returns:
        str: PDF URL or None
    """
    arxiv_id = extract_arxiv_id(paper_info)
    if not arxiv_id:
        return None
    return f"http://arxiv.org/pdf/{arxiv_id}"


def download_paper_text(paper_info):
    """
    Download and extract text from a paper PDF.

    Args:
        paper_info: Either a dict with paper_id/url or a string ID

    Returns:
        dict: {
            "success": bool,
            "message": str,
            "pdf_url": str or None,
            "text": str or None,
            "pages": int
        }
    """
    pdf_url = get_arxiv_pdf_url(paper_info)
    if not pdf_url:
        return {
            "success": False,
            "message": "Not an arXiv paper or invalid paper information",
            "pdf_url": None,
            "text": None,
            "pages": 0
        }

    try:
        response = requests.get(pdf_url)
        response.raise_for_status()

        pdf_file = io.BytesIO(response.content)
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n\n"

        # Cache parsed PDF text by <today>_<arxiv_id>.txt — local artifact
        # of daily_paper's own parsing, reused by downstream consumers
        # (e.g. ~/Desktop/Wiki/daily_paper/sync_from_daily_paper.py).
        try:
            arxiv_id = extract_arxiv_id(paper_info)
            if arxiv_id:
                os.makedirs(PDF_CACHE_DIR, exist_ok=True)
                today = date.today().strftime("%Y-%m-%d")
                cache_path = os.path.join(PDF_CACHE_DIR, f"{today}_{arxiv_id}.txt")
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(text)
        except Exception as e:
            logger.warning(f"PDF cache write failed: {e}")

        return {
            "success": True,
            "message": "Successfully downloaded and extracted text",
            "pdf_url": pdf_url,
            "text": text,
            "pages": num_pages
        }

    except requests.RequestException as e:
        logger.error(f"Error downloading PDF: {e}")
        return {
            "success": False,
            "message": f"Failed to download PDF: {str(e)}",
            "pdf_url": pdf_url,
            "text": None,
            "pages": 0
        }

    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return {
            "success": False,
            "message": f"Failed to extract text: {str(e)}",
            "pdf_url": pdf_url,
            "text": None,
            "pages": 0
        }
