# Search Engine Project

## 1. Introduction
This project implements a simplified search engine based on Section 23.6 of the course textbook (zyBooks — Chapter 23: String Algorithms).  
It indexes a small collection of text/HTML pages, preprocesses the text, builds an inverted index, removes stop words, and performs AND-based keyword search.  
An additional Trie structure is included to support prefix-based suggestions using the command prefix <term>.

This README describes the updated implementation, algorithms, and data structures used in the final version.

------------------------------------------------------------

## 2. Project Structure

SearchEngineProject/
    => data/
        page1.txt
        page2.txt
        page3.txt
        page4.txt
        page5.txt
        page6.txt

    => docs/
        algorithm_explanation.md
        system_design.md
        system_architecture.png

    => output/
        output.txt

    => src/
        tokenizer.py
        parser.py
        inverted_index.py
        trie.py
        search_engine.py
        main.py

    => tests/
        test_tokenizer.py
        test_parser.py
        test_search_engine.py
        test_integration_search_engine.py
        test_advanced_search_engine.py
        test_end_to_end_cli.py

    => README.md
    => requirements.txt
    => .gitignore

------------------------------------------------------------

## 3. Algorithms Used

### 3.1 Tokenization
Text preprocessing includes:
1. Lowercasing  
2. Removing punctuation  
3. Normalizing whitespace  
4. Splitting text into tokens  
5. Removing stop words  

These steps match the intended behavior described in zyBooks and the actual implementation in tokenizer.py.

------------------------------------------------------------

### 3.2 Parsing Input Pages
The parser uses BeautifulSoup to extract visible text from `.txt` or `.html` files.  
If a `<title>` tag exists, its text becomes the page’s title; otherwise, the filename is used.  
The parser ensures only meaningful text is passed to the tokenizer.

------------------------------------------------------------

### 3.3 Inverted Index Construction (Section 23.6)
The inverted index maps:
term -> { document_name : frequency }

For each document:
- The parser extracts visible text  
- The tokenizer produces filtered tokens  
- Each new token is inserted into the Trie  
- The token frequency is updated in the inverted index  

This enables fast reverse lookup for search queries.

------------------------------------------------------------

### 3.4 Searching and Ranking
The search engine implements **strict AND-based search**:

1. Tokenize the user query  
2. If any token does not appear in the inverted index → return empty results  
3. For all present tokens:
   - Retrieve frequency mappings  
4. Compute score(doc) = sum of frequencies of all query terms  
5. Sort results by descending score  

This approach matches the simplified model in Section 23.6 and the actual behavior in search_engine.py.

Note:
This implementation does **not** use set intersection; instead, it uses early failure (if token missing → no results).  
This is consistent with the project's intended AND-search logic.

------------------------------------------------------------

### 3.5 Trie-Based Prefix Search (Enhancement)
A Trie stores all unique terms from the index.

It supports prefix queries:
prefix dat
returns:
data  
database  
datasets  

This feature enhances usability but does not modify AND-search ranking.

------------------------------------------------------------

## 4. Data Structures Used

1. **Dictionary (Hash Table):**  
   Stores inverted index: term → {document: frequency}

2. **Trie:**  
   Stores all unique tokens for prefix lookup

3. **Lists:**  
   Used for tokens, parsed text, and output results

4. **No set-based intersections**  
   The final version uses early termination for AND logic instead of set intersections

All data structures are covered in the textbook.

------------------------------------------------------------

## 5. How to Run the Program

### Install dependencies
pip install -r requirements.txt

### Run the search engine
python3 src/main.py

### Example search
Enter search query: machine learning  
Search Results:  
- page1.txt | Artificial Intelligence and Machine Learning | Score = 11  
- page6.txt | Augmented and Virtual Reality | Score = 2  

### Example prefix search
Enter search query: prefix dat  
Trie Prefix Matches:  
data  
database  
datasets  

------------------------------------------------------------

## 6. Input Files (Required)
The data/ folder contains all indexed pages.  
Files may contain simple text or HTML-like markup.

Example:
<a href="page2.txt">Go to Page 2</a>

------------------------------------------------------------

## 7. Output Files (Required)
The output/ folder contains:

output.txt — contains full sample program runs, including:
- Regular keyword searches  
- Multi-term AND searches  
- Missing-term cases  
- Punctuation and case variations  
- Repeated-term queries  
- Prefix matches  
- Boundary-condition testing  

This file is required for grading.

------------------------------------------------------------

## 8. Boundary Conditions Tested
The final implementation and output.txt include:
- Empty queries  
- Stop-word-only queries  
- Words absent from the dataset  
- Multi-term AND failure  
- Uppercase/lowercase variations  
- Punctuation-heavy queries  
- Repeated-term queries (frequency amplification)  
- Prefix operations  
- Queries mixing relevant and irrelevant words  

All behaviors match the implemented search logic.

------------------------------------------------------------

## 9. Enhancements (Compliant With Requirements)
- Term-frequency scoring  
- Trie prefix search  
- Modular architecture in src/  
- Extended test coverage under tests/  
- Updated documentation under docs/  
- Architecture diagram included  

All enhancements use data structures and algorithms covered in zyBooks.

------------------------------------------------------------

## 10. Author
Vidhi Babariya  
Master of Science in Computer Science  
Stevens Institute of Technology
