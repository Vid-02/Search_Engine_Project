"""
Cleans text and converts it into meaningful tokens for indexing.

Steps:
- Lowercase the text
- Remove punctuation
- Split on whitespace
- Remove common stop words (articles, pronouns, prepositions, etc.)
"""

import string
from typing import List

# Expanded stopword set appropriate for this assignment.
STOP_WORDS = {
    # Articles
    "a", "an", "the",

    # Pronouns
    "i", "me", "you", "he", "him", "she", "her", "it",
    "we", "us", "they", "them",
    "my", "your", "his", "its", "our", "their",
    "this", "that", "these", "those",

    # Prepositions
    "in", "on", "at", "by", "for", "from", "with", "to",
    "of", "into", "over", "under", "between",
    "through", "during", "before", "after",

    # Conjunctions
    "and", "or", "but", "so",

    # Auxiliary verbs
    "is", "are", "was", "were", "be", "am", "been",
    "has", "have", "had", "do", "does", "did",

    # Misc
    "as", "if", "than", "then", "also", "just"
}


def clean_text(text: str) -> str:
    """
    Normalize text by lowercasing and removing punctuation.

    Parameters:-
    text : str
        Raw text extracted from a page.

    Returns:-
    str
        Cleaned text suitable for tokenization.
    """
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return " ".join(text.split())


def tokenize(text: str) -> List[str]:
    """
    Convert cleaned text into individual tokens and remove stop words.

    Parameters:-
    text : str
        Raw or cleaned text.

    Returns:-
    List[str]
        List of tokens to be indexed.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return []

    words = cleaned.split()
    return [w for w in words if w not in STOP_WORDS]
