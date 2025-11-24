"""
inverted_index.py
Implements the inverted index used by the search engine.

Each term maps to the list of documents where it appears, along with
its frequency in each document. This matches the simplified model from
zyBooks Section 23.6.

Additionally, all unique terms are stored inside a Trie so that index
terms can be looked up or matched by prefix if needed.
"""

from collections import defaultdict
from trie import Trie


class InvertedIndex:
    """
    Stores:
    - index:    term -> { document_name : frequency }
    - trie:     stores all unique terms for fast lookup / prefix search
    """

    def __init__(self):
        # term -> {doc: frequency}
        self.index = defaultdict(lambda: defaultdict(int))

        # store all unique terms in Trie
        self.trie = Trie()

    def add_document(self, doc_id: str, tokens: list):
      
        #Insert all tokens from one document into the inverted index.
        for token in tokens:

            # Insert into Trie if term is new
            if token not in self.index:
                self.trie.insert(token)

            # Increase term frequency
            self.index[token][doc_id] += 1

    def search(self, query_tokens: list) -> dict:
        """
        Perform AND-based search:
        A document is returned only if it contains ALL query tokens.
        """
        if not query_tokens:
            return {}

        doc_scores = defaultdict(int)

        # AND logic -> if any token missing, return nothing
        for token in query_tokens:
            if token not in self.index:
                return {}

            for doc, freq in self.index[token].items():
                doc_scores[doc] += freq

        # Sort documents by descending score
        return dict(
            sorted(
                doc_scores.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )
