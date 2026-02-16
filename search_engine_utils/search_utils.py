#!/usr/bin/env python3
"""
Search utilities for fuzzy matching and other search operations
"""

from thefuzz import fuzz


def fuzzy_match(text: str, search_term: str, threshold: int = 60) -> int:
    """
    Fuzzy string matching using thefuzz library's token_set_ratio.
    Returns 1 if similarity score >= threshold, 0 otherwise.

    Uses token_set_ratio which:
    - Handles word order differences
    - Ignores duplicate words
    - Handles partial matches (e.g., "pilsner" matches "Holsten Premium Pilsner")
    - Tolerates typos and variations

    Args:
        text: The text to match against (e.g., beer name, paper title)
        search_term: The search term from user query
        threshold: Minimum similarity score (0-100) to consider a match. Default: 60

    Returns:
        1 if similarity >= threshold, 0 otherwise

    Example:
        >>> fuzzy_match("Grolsch Premium Pilsner", "pilsner")
        1
        >>> fuzzy_match("Guinness Draught", "guiness")  # typo tolerance
        1
        >>> fuzzy_match("Budweiser", "pilsner")
        0
    """
    if text is None or search_term is None:
        return 0

    # Use token_set_ratio for flexible matching
    similarity = fuzz.token_set_ratio(text, search_term)

    # Return 1 if similarity >= threshold, else 0
    return 1 if similarity >= threshold else 0
