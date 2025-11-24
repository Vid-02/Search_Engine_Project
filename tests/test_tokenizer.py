"""
Basic and advanced tests for the tokenizer module.

Checks:
- lowercasing
- punctuation removal
- stopword removal
- hyphen / special char handling
- mixed-case queries
- repeated-word normalization
- handling empty input
"""

from tokenizer import clean_text, tokenize


def test_clean_text_basic():
    # Basic lowercase + punctuation removal
    assert clean_text("Hello, World!") == "hello world"


def test_clean_text_extra_spaces():
    # Multiple spaces should be collapsed
    assert clean_text("AI     ML   is   fun") == "ai ml is fun"


def test_tokenize_stopwords_removed():
    # Stopwords like "the", "and", "are" should be removed
    tokens = tokenize("The machine and the system are powerful")
    assert tokens == ["machine", "system", "powerful"]


def test_tokenize_punctuation_handling():
    # Punctuation should be removed cleanly
    tokens = tokenize("AI, ML; and data-science!")
    assert tokens == ["ai", "ml", "datascience"]


def test_tokenize_hyphenated_words():
    # Hyphens should be merged into single tokens
    tokens = tokenize("state-of-the-art models")
    assert tokens == ["stateoftheart", "models"]


def test_tokenize_mixed_case_words():
    # Case-insensitive tokenization
    tokens = tokenize("MaChInE LeArNiNg")
    assert tokens == ["machine", "learning"]


def test_tokenize_repeated_words():
    # Repeated words should all appear (no deduplication in tokenizer)
    tokens = tokenize("data DATA Data")
    assert tokens == ["data", "data", "data"]


def test_tokenize_empty_string():
    # Empty input -> no tokens
    assert tokenize("") == []
