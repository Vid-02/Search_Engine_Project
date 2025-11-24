"""
Entry point for running the simplified search engine.

Tasks performed:
- Initialize the SearchEngine
- Build the index from the data/ directory
- Accept user queries
- Run searches and display results
- Provide optional prefix matching through the Trie
"""

from search_engine import SearchEngine


def main():
    print("Building search index...")
    engine = SearchEngine(data_folder="data")
    engine.build_index()

    print("\nSearch Engine Ready.")
    print("Type a query OR:")
    print("  prefix <text>   → Trie prefix search (optional)")
    print("  exit            → quit the program\n")

    while True:
        query = input("Enter search query: ").strip()

        # Exit command
        if query.lower() == "exit":
            print("Exiting search engine.")
            break

        # Prefix search (Trie-based)
        if query.lower().startswith("prefix "):
            prefix = query[7:].strip()
            matches = engine.prefix_search(prefix)

            if not matches:
                print("No terms found with that prefix.\n")
            else:
                print("Trie Prefix Matches:")
                for term in matches:
                    print(f"- {term}")
                print()
            continue

        # Standard search
        if not query:
            print("Empty query. Please enter a valid search.\n")
            continue

        results = engine.search(query)

        if not results:
            print("No matching documents found.\n")
            continue

        print("\nSearch Results:")
        for doc, title, score in results:
            print(f"- {doc} | {title} | Score = {score}")
        print()


if __name__ == "__main__":
    main()
