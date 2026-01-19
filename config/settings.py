"""
Configuration settings for daily_paper project.

Centralized configuration for API settings, paths, and processing parameters.
"""
import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# ==================== PROJECT PATHS ====================
PROJECT_ROOT = Path(__file__).parent.parent
DAILIES_DIR = PROJECT_ROOT / 'dailies'
PAGES_DIR = DAILIES_DIR / 'pages'
NOTES_DIR = DAILIES_DIR / 'notes'
IMAGES_DIR = DAILIES_DIR / 'images'
BG_DIR = PROJECT_ROOT / 'bg'
TEMPLATES_DIR = PROJECT_ROOT / 'templates'

# Data files
SUMMARIES_FILE = PROJECT_ROOT / 'summaries.jsonl'


# ==================== API CREDENTIALS ====================
# AI Gateway
GENAI_GATEWAY_API_KEY = os.getenv("GENAI_GATEWAY_API_KEY")

# Google Chat
GOOGLE_CHAT_SPACE_ID = os.getenv("SPACE_ID")
GOOGLE_CHAT_KEY = os.getenv("KEY")

# Testing mode
TEST_MODE = os.getenv("TEST", "TRUE").upper() == "TRUE"


# ==================== PROCESSING PARAMETERS ====================
# Paper processing
MAX_PAPER_LENGTH = 12000  # Maximum word count for papers
PAPER_COUNTS = 3  # Number of papers to process per day
GRAB_NUMBER = 100  # Number of papers to fetch from HuggingFace
RANK_METHOD = 'hot'  # Sorting method: 'hot', 'rising', or 'new'

# Timeouts (in seconds)
PAPER_PROCESSING_TIMEOUT = 150
THREAD_JOIN_TIMEOUT = 30


# ==================== AI MODEL SETTINGS ====================
# Default models for different tasks
DEFAULT_SUMMARY_MODEL = 'claude35'  # For paper summaries
DEFAULT_QUIZ_MODEL = 'claude35'  # For quiz generation
DEFAULT_FLOWCHART_MODEL = 'claude4'  # For flowchart generation

# Model parameters
AI_TEMPERATURE = 0.8
AI_MAX_TOKENS = 8192
AI_SAFETY_FILTERING = 'off'


# ==================== GITHUB PAGES SETTINGS ====================
GITHUB_PAGES_BASE_URL = 'https://xinzhang-ops.github.io/daily_paper'
GITHUB_PAGES_SUBDOMAIN = 'dailies/pages'


# ==================== HTML GENERATION SETTINGS ====================
# Background images for paper cards
BACKGROUND_IMAGES = [
    'argyle.png',
    'black-linen-2.png',
    'black-lozenge.png',
    'black-orchid.png',
    'black-paper.png',
    'broken-noise.png',
    'buried.png',
    'dark-geometric.png',
    'dark-wood.png',
    'diagmonds.png',
    'my-little-plaid-dark.png',
    'office.png',
    'robots.png',
    'shattered-dark.png',
    'shley-tree-1.png',
    'shley-tree-2.png',
    'stressed-linen.png',
    'tasky.png',
    'tileable-wood-colored.png',
    'tileable-wood.png',
    'type.png',
    'use-your-illusion.png',
    'woven.png',
]


# ==================== EXTERNAL APIs ====================
HUGGINGFACE_API_URL = 'https://huggingface.co/api/daily_papers'
QUOTE_API_URL = 'https://api.quotable.io/quotes/random'
ARXIV_PDF_URL_TEMPLATE = 'http://arxiv.org/pdf/{arxiv_id}'


# ==================== VALIDATION ====================
def validate_config():
    """
    Validate that required configuration is present.

    Raises:
        ValueError: If required configuration is missing
    """
    errors = []

    if not GENAI_GATEWAY_API_KEY:
        errors.append("GENAI_GATEWAY_API_KEY not set in environment")

    if not GOOGLE_CHAT_SPACE_ID:
        errors.append("SPACE_ID not set in environment")

    if not GOOGLE_CHAT_KEY:
        errors.append("KEY not set in environment")

    if errors:
        raise ValueError(
            "Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors)
        )


# ==================== DIRECTORY INITIALIZATION ====================
def ensure_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        DAILIES_DIR,
        PAGES_DIR,
        NOTES_DIR,
        IMAGES_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    # Test configuration
    print("Configuration loaded successfully!")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Test mode: {TEST_MODE}")
    print(f"Paper processing: {PAPER_COUNTS} papers, max {MAX_PAPER_LENGTH} words")

    try:
        validate_config()
        print("✓ All required configuration is present")
    except ValueError as e:
        print(f"✗ Configuration validation failed:\n{e}")

    ensure_directories()
    print("✓ All directories created/verified")
