"""
End-to-end tests for the CLI interface of the search engine.

These tests simulate how a user interacts with the program:
- typing queries
- prefix search
- empty input handling
- unknown queries
- exiting the program

They verify the actual printed output, not just internal functions.
"""

import tempfile
import os
import builtins
from main import main
from search_engine import SearchEngine


def create_page(tmp, name, content):
    #Helper: create a page inside a temporary directory.
    path = os.path.join(tmp, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def test_cli_basic_search(monkeypatch, capsys):
    #Simulate a user performing a basic search via the CLI.

    with tempfile.TemporaryDirectory() as tmp:
        create_page(tmp, "a.txt", "<p>machine learning</p>")
        create_page(tmp, "b.txt", "<p>deep learning</p>")

        # Build the index before running main (CLI only handles searching)
        engine = SearchEngine(tmp)
        engine.build_index()

        # Simulated user input: search -> exit
        inputs = iter(["machine", "exit"])
        monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

        # run the actual CLI
        main()  

        out = capsys.readouterr().out
        assert "Search Results:" in out
        assert "a.txt" in out
        assert "Exiting search engine." in out


def test_cli_prefix_search(monkeypatch, capsys):
    #Simulate prefix search through the CLI.

    with tempfile.TemporaryDirectory() as tmp:
        create_page(tmp, "p1.txt", "<p>run runner running</p>")

        SearchEngine(tmp).build_index()

        inputs = iter(["prefix run", "exit"])
        monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

        main()
        out = capsys.readouterr().out

        assert "Trie Prefix Matches:" in out
        assert "run" in out
        assert "Exiting search engine." in out


def test_cli_empty_query(monkeypatch, capsys):
    #User enters an empty query; CLI should prompt again.

    with tempfile.TemporaryDirectory() as tmp:
        create_page(tmp, "p1.txt", "<p>example text</p>")

        SearchEngine(tmp).build_index()

        inputs = iter(["", "example", "exit"])
        monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

        main()
        out = capsys.readouterr().out

        assert "Empty query" in out
        assert "Search Results:" in out


def test_cli_unknown_search(monkeypatch, capsys):
    #Unknown term should produce 'No matching documents found.'

    with tempfile.TemporaryDirectory() as tmp:
        create_page(tmp, "p1.txt", "<p>machine learning</p>")

        SearchEngine(tmp).build_index()

        inputs = iter(["quantum", "exit"])
        monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

        main()
        out = capsys.readouterr().out

        assert "No matching documents found." in out
        assert "Exiting search engine." in out
