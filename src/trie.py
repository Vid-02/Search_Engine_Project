"""
Implements a simple Trie (prefix tree) for storing index terms.

Why Trie?

zyBooks Section 23.6 discusses storing index terms in a Trie (or compressed Trie)
to support fast lookup of terms and prefixes. This Trie is used by the inverted
index to store every unique token encountered during indexing.

Supported Operations:

1. insert(term)          : Insert a full term into the Trie.
2. search_exact(term)    : Check whether a term exists in the Trie.
3. search_prefix(prefix) : Return all stored terms that begin with a prefix.
"""

from __future__ import annotations
from typing import Dict, List, Optional


class TrieNode:
    """
    A single node in the Trie.

    Attributes:-
    
    children : Dict[str, TrieNode]
        Maps a character to its child TrieNode.
    is_end_of_word : bool
        True if this node marks the end of an inserted word.
    term : Optional[str]
        Stores the complete word at terminal nodes (useful for prefix results).
    """
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False
        self.term: Optional[str] = None


class Trie:
    """
    Trie data structure for index terms.

    The Trie stores words character-by-character.
    Time complexity:
    - insert(term): O(m)
    - search_exact(term): O(m)
    where m is the length of the term.
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, term: str) -> None:
        """
        Insert a term into the Trie.

        Parameters:-
        term : str
            The lowercase token to insert.
        """
        node = self.root

        # Walk down the Trie, creating nodes as needed
        for char in term:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        # Mark the end of the word and store the full term
        node.is_end_of_word = True
        node.term = term

    def search_exact(self, term: str) -> bool:
        """
        Check if an exact term exists in the Trie.

        Parameters:-
        term : str
            Term to look up.

        Returns:-
        bool
            True if the term was inserted before; False otherwise.
        """
        node = self.root

        for char in term:
            if char not in node.children:
                return False
            node = node.children[char]

        return node.is_end_of_word

    def search_prefix(self, prefix: str) -> List[str]:
        """
        Return all stored terms that start with the given prefix.

        Parameters:-
        prefix : str
            Prefix to search for.

        Returns:-
        List[str]
            All terms in the Trie that begin with prefix.
        """
        node = self.root

        # Move to the node representing the prefix
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # Collect all terms below this prefix node
        results: List[str] = []
        self._collect_terms(node, results)
        return results

    def _collect_terms(self, node: TrieNode, results: List[str]) -> None:
    
        #Helper DFS to collect all terms under a given node.    
        if node.is_end_of_word and node.term is not None:
            results.append(node.term)

        for child in node.children.values():
            self._collect_terms(child, results)
