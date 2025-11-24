"""
Basic tests for the SearchEngine class.

Covers:
- index building
- single-term queries
- multi-term AND logic
- term-frequency ranking
- empty queries
- stopword-only queries
- missing-term queries
"""

import tempfile
import os
from search_engine import SearchEngine


def create_page(tmpdir, filename, content):
    # Helper: create a page inside a temporary directory
    path = os.path.join(tmpdir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def test_basic_indexing_and_single_term_search():
    # Search engine should index pages and return results for simple queries
    with tempfile.TemporaryDirectory() as tmp:
        create_page(tmp, "p1.txt", "<p>Machine learning is powerful.</p>")
        create_page(tmp, "p2.txt", "<p>Learning systems require data.</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("machine")
        assert len(results) == 1
        assert results[0][0] == "p1.txt"


def test_and_search_returns_only_docs_with_all_terms():
    # AND logic: returns only docs containing *all* query terms
    with tempfile.TemporaryDirectory() as tmp:
        create_page(tmp, "p1.txt", "<p>Machine learning and data science.</p>")
        create_page(tmp, "p2.txt", "<p>Machine systems exist.</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("machine learning")
        assert len(results) == 1
        assert results[0][0] == "p1.txt"


def test_ranking_prefers_higher_frequency():
    # Document containing the term more often should rank higher
    with tempfile.TemporaryDirectory() as tmp:
        create_page(tmp, "p1.txt", "<p>data data analysis</p>")
        create_page(tmp, "p2.txt", "<p>data science</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("data")
        assert results[0][0] == "p1.txt"
        assert results[1][0] == "p2.txt"


def test_empty_query_returns_no_results():
    # Empty input should not produce results
    with tempfile.TemporaryDirectory() as tmp:
        create_page(tmp, "p1.txt", "<p>Example content.</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        assert engine.search("") == []


def test_stopword_only_query_returns_no_results():
    # Query with only stopwords -> no tokens -> no results
    with tempfile.TemporaryDirectory() as tmp:
        create_page(tmp, "p1.txt", "<p>Some content here.</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        assert engine.search("the and was") == []


def test_query_with_missing_term_returns_empty():
    # Query contains a word not present in any doc -> no results
    with tempfile.TemporaryDirectory() as tmp:
        create_page(tmp, "p1.txt", "<p>Machine learning example.</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        assert engine.search("quantum") == []
