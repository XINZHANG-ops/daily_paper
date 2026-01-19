"""
Configuration package for daily_paper project.

Provides centralized configuration settings.
"""
from .settings import (
    # Paths
    PROJECT_ROOT,
    DAILIES_DIR,
    PAGES_DIR,
    NOTES_DIR,
    IMAGES_DIR,
    BG_DIR,
    TEMPLATES_DIR,
    SUMMARIES_FILE,

    # API Credentials
    GENAI_GATEWAY_API_KEY,
    GOOGLE_CHAT_SPACE_ID,
    GOOGLE_CHAT_KEY,
    TEST_MODE,

    # Processing Parameters
    MAX_PAPER_LENGTH,
    PAPER_COUNTS,
    GRAB_NUMBER,
    RANK_METHOD,
    PAPER_PROCESSING_TIMEOUT,

    # AI Model Settings
    DEFAULT_SUMMARY_MODEL,
    DEFAULT_QUIZ_MODEL,
    DEFAULT_FLOWCHART_MODEL,
    AI_TEMPERATURE,
    AI_MAX_TOKENS,

    # GitHub Pages
    GITHUB_PAGES_BASE_URL,

    # Background Images
    BACKGROUND_IMAGES,

    # Functions
    validate_config,
    ensure_directories,
)

__all__ = [
    'PROJECT_ROOT',
    'DAILIES_DIR',
    'PAGES_DIR',
    'NOTES_DIR',
    'IMAGES_DIR',
    'BG_DIR',
    'TEMPLATES_DIR',
    'SUMMARIES_FILE',
    'GENAI_GATEWAY_API_KEY',
    'GOOGLE_CHAT_SPACE_ID',
    'GOOGLE_CHAT_KEY',
    'TEST_MODE',
    'MAX_PAPER_LENGTH',
    'PAPER_COUNTS',
    'GRAB_NUMBER',
    'RANK_METHOD',
    'PAPER_PROCESSING_TIMEOUT',
    'DEFAULT_SUMMARY_MODEL',
    'DEFAULT_QUIZ_MODEL',
    'DEFAULT_FLOWCHART_MODEL',
    'AI_TEMPERATURE',
    'AI_MAX_TOKENS',
    'GITHUB_PAGES_BASE_URL',
    'BACKGROUND_IMAGES',
    'validate_config',
    'ensure_directories',
]
