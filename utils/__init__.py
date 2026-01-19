"""
Utils package for daily_paper project.

This package contains modular utility functions organized by domain:
- ai_utils: AI model interactions (summaries, quizzes, flowcharts)
- huggingface_utils: HuggingFace API interactions
- arxiv_utils: arXiv PDF downloading and processing
- google_chat_utils: Google Chat webhook integrations
- html_utils: HTML/markdown rendering utilities
- file_utils: File I/O operations
- models: AI model configuration and abstraction
"""

from .models import model_response, model_map
from .huggingface_utils import get_huggingface_papers
from .arxiv_utils import download_paper_text, extract_arxiv_id, get_arxiv_pdf_url
from .ai_utils import summary_paper, create_question, create_flow_chart, process_paper, extract_categories
from .google_chat_utils import send_articles, start_thread
from .file_utils import find_not_proposed_papers, load_daily_takeaways

__all__ = [
    'model_response',
    'model_map',
    'get_huggingface_papers',
    'download_paper_text',
    'extract_arxiv_id',
    'get_arxiv_pdf_url',
    'summary_paper',
    'create_question',
    'create_flow_chart',
    'process_paper',
    'extract_categories',
    'send_articles',
    'start_thread',
    'find_not_proposed_papers',
    'load_daily_takeaways',
]
