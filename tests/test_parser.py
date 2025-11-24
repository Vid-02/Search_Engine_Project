"""
Tests for the parser module.

Checks:
- HTML parsing
- Tag stripping
- Extracting <title>
- Handling pages without <title>
- Nested + malformed HTML
"""

import tempfile
import os
from parser import load_page


def create_temp_page(content: str):
    # Helper to create a temporary HTML/text page
    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=".txt", mode="w", encoding="utf-8"
    )
    tmp.write(content)
    tmp.close()
    return tmp.name


def test_extracts_title_correctly():
    # Page with <title> should return that title
    html = "<html><head><title>My Page</title></head><body>Text here</body></html>"
    path = create_temp_page(html)

    title, text = load_page(path)
    assert title == "My Page"
    assert "Text here" in text

    os.remove(path)


def test_no_title_falls_back_to_filename():
    # If <title> missing, fallback should be filename (not full path)
    html = "<html><body>No title here</body></html>"
    path = create_temp_page(html)

    title, text = load_page(path)
    assert title == os.path.basename(path)
    assert "No title here" in text

    os.remove(path)


def test_strips_tags_and_keeps_visible_text():
    # HTML tags should be removed while visible text remains
    html = "<html><body><h1>Header</h1><p>Paragraph text</p></body></html>"
    path = create_temp_page(html)

    title, text = load_page(path)
    assert "Header" in text
    assert "Paragraph text" in text

    os.remove(path)


def test_parses_nested_html():
    # Nested tags should still yield correct visible text
    html = "<div><p>Nested <span>inside</span> content</p></div>"
    path = create_temp_page(html)

    title, text = load_page(path)
    assert "Nested inside content" in text

    os.remove(path)


def test_handles_malformed_html_gracefully():
    # Malformed HTML should not crash parser
    html = "<html><body><p>Broken <div>HTML"
    path = create_temp_page(html)

    title, text = load_page(path)
    assert "Broken" in text
    assert "HTML" in text

    os.remove(path)
