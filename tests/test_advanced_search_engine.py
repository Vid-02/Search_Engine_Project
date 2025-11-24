"""
test_advanced_search_engine.py
Advanced tests for the search engine.

Covers:
- complex AND search
- mixed stopwords + valid terms
- punctuation-heavy queries
- repeated-term queries
- case-insensitive behavior
- multi-document ranking edge cases
- Trie/prefix behavior in search engine context
- malformed and nested HTML integration
"""

import tempfile
import os
from search_engine import SearchEngine


def write(tmpdir, filename, content):
    # Helper: create a test page inside the temporary site directory
    path = os.path.join(tmpdir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path



# Complex AND search behaviour

def test_and_search_with_stopwords_mixed_inside():
    # Stopwords should be removed, valid terms retained
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "p1.txt", "<p>machine learning system</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("the machine and system at")
        assert len(results) == 1
        assert results[0][0] == "p1.txt"


def test_and_search_partial_missing_term():
    # AND logic: if one term missing -> no results
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "p1.txt", "<p>deep learning models</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("deep quantum")
        assert results == []


# Case-insensitivity & punctuation

def test_search_is_case_insensitive():
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "p1.txt", "<p>Neural Networks</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("nEUral")
        assert len(results) == 1
        assert results[0][0] == "p1.txt"


def test_query_with_punctuation_is_cleaned():
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "p1.txt", "<p>data science pipeline</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("data,")
        assert len(results) == 1
        assert results[0][0] == "p1.txt"


def test_repeated_terms_still_work():
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "p1.txt", "<p>data data data science</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("data data data")
        assert results[0][0] == "p1.txt"



# Multi-document ranking edge cases

def test_ranking_with_multiple_documents():
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "a.txt", "<p>data data analysis</p>")
        write(tmp, "b.txt", "<p>data science data</p>")
        write(tmp, "c.txt", "<p>data</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("data")
        order = [doc for doc, title, score in results]

        # highest -> lowest score
        assert order[-1] == "c.txt"
        assert "a.txt" in order and "b.txt" in order


def test_ranking_when_all_docs_match_all_terms():
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "a.txt", "<p>machine learning</p>")
        write(tmp, "b.txt", "<p>machine learning learning</p>")
        write(tmp, "c.txt", "<p>machine machine learning</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("machine learning")
        assert len(results) == 3

        # a.txt should be last (lowest freq)
        assert results[-1][0] == "a.txt"



# Trie prefix matching inside search context

def test_prefix_search_multiple_matches():
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "p1.txt", "<p>run runner running</p>")
        write(tmp, "p2.txt", "<p>running fast</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        matches = engine.prefix_search("run")
        assert len(matches) >= 2
        assert any(term.startswith("run") for term in matches)


def test_prefix_search_case_insensitive():
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "p1.txt", "<p>Neural network</p>")

        engine = SearchEngine(tmp)
        engine.build_index()

        matches = engine.prefix_search("NEU")
        assert "neural" in matches



# Parser integration (nested/malformed HTML)

def test_nested_html_content_is_extracted():
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "p1.txt", "<div><p>Nested <span>inside</span> content</p></div>")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("inside")
        assert len(results) == 1


def test_malformed_html_is_handled_gracefully():
    with tempfile.TemporaryDirectory() as tmp:
        write(tmp, "p1.txt", "<p>Broken <div>HTML")

        engine = SearchEngine(tmp)
        engine.build_index()

        results = engine.search("broken")
        assert len(results) == 1
