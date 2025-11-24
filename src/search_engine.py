"""
Coordinates the main components of the simplified search engine.

Responsibilities:
- Scan the data/ directory
- Load and parse each page
- Tokenize extracted text
- Build the inverted index (which also updates the Trie)
- Run AND-based ranked searches
- Provide optional prefix search using the Trie
"""

import os
from parser import load_page
from tokenizer import tokenize
from inverted_index import InvertedIndex


class SearchEngine:
    """
    Controller for indexing pages and running searches.
    Includes:
    - Inverted index (term -> docs)
    - Trie storage for unique terms
    - Document titles for cleaner output
    """

    def __init__(self, data_folder: str):
        self.data_folder = data_folder
        self.index = InvertedIndex()
        self.titles = {}   # doc_id -> title

    def build_index(self):
        """
        Build the inverted index by processing every .txt/.html file
        in the data folder.
        """
        for filename in os.listdir(self.data_folder):
            if filename.endswith(".txt") or filename.endswith(".html"):
                filepath = os.path.join(self.data_folder, filename)

                # Parse the file and extract title + text
                title, text = load_page(filepath)
                self.titles[filename] = title

                # Tokenize the text and add to the index
                tokens = tokenize(text)
                self.index.add_document(filename, tokens)

        print("Index successfully built.")
        print(
            f"Total unique Trie terms: "
            f"{len(self.index.trie.search_prefix(''))}"
        )

    def _apply_trie_fallback(self, tokens):
        """
        For each token:
        - If exact match exists -> keep it
        - Else use Trie prefix match (first match)
        - Else return [] meaning AND-search must fail
        """
        fallback_tokens = []

        for word in tokens:
            # If exact token exists -> use it
            if word in self.index.index:
                fallback_tokens.append(word)
                continue

            # Try trie prefix fallback
            matches = self.index.trie.search_prefix(word)
            if matches:
                fallback_tokens.append(matches[0])   # deterministic choice
            else:
                return []   # AND logic -> whole search fails

        return fallback_tokens

    def search(self, query: str) -> list:
        """
        Run a standard AND-based search on the inverted index, with
        optional Trie prefix fallback when exact tokens do not exist.

        Returns:-
        list of (doc_id, title, score)
        """
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        # Apply Trie fallback for near-matching tokens
        final_tokens = self._apply_trie_fallback(query_tokens)
        if not final_tokens:
            return []

        results = self.index.search(final_tokens)

        formatted_results = []
        for doc, score in results.items():
            title = self.titles.get(doc, doc)
            formatted_results.append((doc, title, score))

        return formatted_results

    def prefix_search(self, prefix: str) -> list:
        """
        Optional: Use the Trie to find all terms starting with a prefix.
        Useful for suggestions or interactive exploration.
        """
        prefix = prefix.strip().lower()
        if not prefix:
            return []

        return self.index.trie.search_prefix(prefix)
