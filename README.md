# Search Engine Project

## 1. Introduction
This project implements a simplified search engine as described in Section 23.6 (Search Engines) of the course textbook (zyBooks — Chapter 23: String Algorithms). It indexes the pages of a small website and supports keyword-based search using an inverted index, while excluding stop words such as articles, prepositions, and pronouns.

This README explains the approach, algorithms, data structures, and program flow used in the project.

## 2. Project Structure

SearchEngineProject/
│
├── data/
│   ├── page1.txt
│   ├── page2.txt
│   └── page3.txt
│
├── docs/
│   ├── algorithm_explanation.md
│   ├── system_design.md
│   └── index_diagram.png
│
├── output/
│   ├── logs.txt
│   └── results_example.txt
│
├── src/
│   ├── tokenizer.py
│   ├── parser.py
│   ├── inverted_index.py
│   ├── search_engine.py
│   └── main.py
│
├── tests/
│   ├── test_tokenizer.py
│   ├── test_parser.py
│   └── test_search_engine.py
│
├── README.md
├── requirements.txt
└── .gitignore

## 3. Algorithms Used

### 3.1 Tokenization
Each page is processed through:
1. Lowercasing
2. Removing punctuation
3. Splitting into words
4. Removing stop words (articles, pronouns, prepositions)

### 3.2 Parsing Input Pages
The project uses BeautifulSoup (allowed by instructor guidelines) to extract visible text from simple HTML-like pages.

### 3.3 Inverted Index Construction (Section 23.6)
The system builds a dictionary:

term → { document_name: frequency }

This inverted index consists of:
- a dictionary of terms
- an occurrence list for each term

Python's dict is used as a hash-based dictionary, consistent with textbook data structures.

### 3.4 Searching and Ranking
Searching follows the process described in Section 23.6:
1. Tokenize the query.
2. Retrieve each term’s occurrence list.
3. Compute intersection of lists (AND search).
4. Rank pages using a simple term-frequency score.

This ranking method is explicitly allowed in the assignment.

## 4. Data Structures Used

1. Dictionary (Hash Table): stores the inverted index.
2. Sets: used to compute intersections for multi-word queries.
3. Lists: used to store raw tokens and intermediate results.

All data structures are covered in the textbook.

## 5. How to Run the Program

### Install dependencies
pip install -r requirements.txt

### Run the search engine
python3 src/main.py

### Example
Enter query: search engine  
Found in:  
- page1.txt | Score = 5  
- page3.txt | Score = 2  

## 6. Input Files (Required)
The data/ folder contains sample web pages in simple HTML-like text format. Each page includes at least one hyperlink to another page, as required.

Example hyperlink syntax:
<a href="page2.txt">Go to Page 2</a>

## 7. Output Files (Required)
Inside output/:
- results_example.txt: sample search results
- logs.txt: optional logs for debugging

These files demonstrate that the program runs as expected.

## 8. Boundary Conditions Tested
- Query containing only stop words
- Empty query
- Query term not found in any document
- Term appearing in only one document
- Pages with overlapping terms

## 9. Enhancements (Still Compliant)
To make the project more professional, the following optional enhancements were added:
- Term frequency ranking
- Clean modular architecture in src/
- Simple unit tests in tests/
- Documentation in docs/

All enhancements follow the requirement: “Use only algorithms and data structures covered in the textbook.”

## 10. Author
Vidhi Babariya  
Master of Science in Computer Science  
Stevens Institute of Technology