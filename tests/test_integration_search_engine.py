"""
Integration tests for the full search engine pipeline.

Covers:
- parser + tokenizer + index + trie working together
- realistic multi-page website behavior
- prefix search in live context
- ranking across many documents
- complex multi-word queries
- handling large text blocks
"""

import tempfile
import os
from search_engine import SearchEngine


def write(tmpdir, filename, content):
    # Helper: creates a test page inside the temporary directory
    path = os.path.join(tmpdir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def test_integration_basic_end_to_end():
    # Tests a simple multi-page scenario
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "about.html", "<h1>About AI</h1> AI research grows rapidly.")
        write(tmp, "ml.html", "<p>Machine learning improves AI.</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("ai")
        docs = [doc for doc, title, score in results]

        assert "about.html" in docs
        assert "ml.html" in docs
        assert len(results) == 2


def test_integration_multi_term_with_stopwords():
    # Stopwords are removed, but meaningful terms are kept
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "page1.html", "<p>Deep learning models rely on data.</p>")
        write(tmp, "page2.html", "<p>Learning improves accuracy.</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("deep on learning")
        assert len(results) == 1
        assert results[0][0] == "page1.html"


def test_integration_parsing_nested_html():
    # Tests nested tags + real extraction
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "weird.html", """
        <html>
            <head><title>Weird</title></head>
            <body>
                <div><p>Nested <span>inside</span> content</p></div>
                <p>More content here.</p>
            </body>
        </html>
        """)

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("inside")
        assert len(results) == 1
        assert results[0][0] == "weird.html"


def test_integration_prefix_and_search_combination():
    # Trie prefix search + standard search both tested
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "page1.txt", "<p>run runner running</p>")
        write(tmp, "page2.txt", "<p>running fast improves stamina</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        prefix_matches = engine.prefix_search("run")
        assert len(prefix_matches) >= 2

        search_results = engine.search("running")
        assert len(search_results) == 2


def test_integration_multi_document_ranking():
    # Ranking accuracy across multiple pages
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "a.txt", "<p>data data analysis</p>")
        write(tmp, "b.txt", "<p>data science data</p>")
        write(tmp, "c.txt", "<p>data</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("data")
        docs = [doc for doc, title, score in results]

        # Highest -> lowest frequency
        assert docs[-1] == "c.txt"
        assert "a.txt" in docs and "b.txt" in docs


def test_integration_large_text_block():
    # Tests large repeated content + long queries
    large_text = "machine " * 50 + "learning " * 30 + "system"
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "big.html", f"<p>{large_text}</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("machine learning system")
        assert len(results) == 1
        assert results[0][0] == "big.html"
        # Score = 50 + 30 + 1 = 81
        assert results[0][2] == 81
