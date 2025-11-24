"""
Responsible for loading each page file and extracting clean, readable text.

This module satisfies the project requirement:
"Use BeautifulSoup in Python for reading web pages."

BeautifulSoup is used to:
- Remove HTML tags safely
- Extract optional <title> content
- Return visible, human-readable text
"""

import os
from bs4 import BeautifulSoup


def load_page(filepath: str) -> tuple[str, str]:
    """
    Load and parse a page file (HTML or plain text).

    Parameters:-
    filepath : str
        The full path to the file inside the data/ directory.

    Returns:-
    tuple[str, str]
        title          - extracted <title> text or the file name
        text_content   - visible cleaned text returned for tokenization
    """
    try:
        # Read the entire file
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return ("[Unreadable File]", "")

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Remove irrelevant tags such as <script> or <style>
    for tag in soup(["script", "style"]):
        tag.extract()

    # Extract page title, else use filename
    title_tag = soup.find("title")
    title = (
        title_tag.get_text().strip()
        if title_tag
        else os.path.basename(filepath)
    )

    # Extract all visible text with normalized spacing
    text = soup.get_text(separator=" ", strip=True)

    return title, text
