# Algorithm Explanation – Simplified Search Engine

This document explains the algorithms used to build the simplified Search Engine for this project.  
The design follows zyBooks Chapter 23, Section 23.6 (Search Engines).  
The system also includes an optional Trie for prefix searching.

-----------------------------

## 1. Overview

The search engine works through the following algorithmic steps:

1. Extract text from pages using an HTML parser.
2. Preprocess text (lowercase, remove punctuation, normalize spaces).
3. Tokenize text and remove stop words.
4. Construct an inverted index.
5. Insert unique terms into a Trie (optional prefix feature).
6. Process AND-based search queries.
7. Rank documents by term frequency.

-----------------------------

## 2. Text Preprocessing Algorithm

Text preprocessing ensures that all documents and queries are normalized before indexing or searching.

Steps:
1. Convert the entire text to lowercase.
2. Remove punctuation using `str.translate()`.
3. Collapse multiple spaces into single spaces.
4. Split the cleaned text into tokens.
5. Remove stop words such as: "the", "is", "in", "at", "of", "with", etc.

Result:
A list of clean tokens ready for indexing.

-----------------------------

## 3. HTML Parsing Algorithm

The parser supports both `.txt` and `.html` files.

Algorithm:
1. Read the file with UTF-8 encoding.
2. Use BeautifulSoup to parse HTML content.
3. Extract the title from the `<title>` tag if present.
4. Extract visible text using `soup.get_text(separator=" ", strip=True)`.
5. Pass the text to the tokenizer.

This ensures that only readable content is indexed.

-----------------------------

## 4. Inverted Index Construction Algorithm

The inverted index maps each term to the documents in which it appears.

Structure:
term → { document_name : frequency }

For each document:
1. Tokenize the document text.
2. For each token:
   - If it is the first occurrence of the token, insert it into the Trie.
   - Increment its frequency:
     index[token][doc_id] += 1

Purpose:
- Fast lookup of documents containing each term.
- Support for ranking based on term frequency.

-----------------------------

## 5. Trie Construction (Optional Feature)

The Trie stores all unique terms for prefix-based queries.

Algorithm:
1. Insert each new word character by character.
2. Use a boolean `is_end` flag to mark complete words.
3. For prefix searching:
   - Traverse the Trie to reach the end of the prefix.
   - Collect all completions using depth-first search.

The Trie does not affect AND-search or ranking; it is used only for prefix suggestions.

-----------------------------

## 6. Query Processing and Ranking Algorithm

Search is AND-based, meaning all query tokens must appear in a document.

Algorithm:
1. Tokenize the user query.
2. If any token is missing from the index, return no results.
3. Otherwise, accumulate scores:
   score(doc) = sum of frequencies of all query tokens.
4. Sort documents in descending order of score.

Example:
Query: machine learning

Possible scores:
page1.txt → 11  
page6.txt → 2

Higher frequency contributes to higher ranking.

-----------------------------

## 7. Summary

This search engine implements:
- Text cleaning
- Tokenization
- Stop-word removal
- HTML parsing
- Inverted index construction
- Optional Trie for prefix searching
- AND-based query processing
- Ranking based on term frequency

These steps match the simplified search engine model described in zyBooks Chapter 23, with an additional Trie enhancement for prefix queries.

