from os import system as cmd
try: 
    from fuzzywuzzy import fuzz
except:
    cmd("pip install fuzzywuzzy")
    from fuzzywuzzy import fuzz
import unicodedata

# Function to normalize and remove accents
def normalize_unicode(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

def search_books(cursor, search_query: str, threshold=40):
    """
    Search for books based on a query with fuzzy matching, accounting for duplicates.
    
    Parameters:
        cursor: Database cursor to execute SQL queries.
        search_query: The user query for searching books.
        threshold: Minimum match score for fuzzy matching (default: 40).
    
    Returns:
        A tuple containing:
        - A list of all valid book IDs.
        - A list of tuples (book_id, rank), sorted by rank in descending order.
    """
    # Normalize and split the search query into keywords
    keywords = normalize_unicode(search_query.lower()).split()

    # Fetch all titles and IDs from the database
    cursor.execute("SELECT id, title, use FROM books")
    all_books = cursor.fetchall()  # (id, title, use)

    # List to store matched results with their scores
    ranked_results = []

    # Iterate through books and calculate match scores
    for book_id, title, use in all_books:
        # Normalize title and additional use field
        title_normalized = normalize_unicode(title.lower())
        use_normalized = normalize_unicode(use.lower())

        # Compute total match score for the book
        total_match_score = 0
        for keyword in keywords:
            total_match_score += fuzz.partial_ratio(keyword, title_normalized)
            total_match_score += 2 * fuzz.partial_ratio(keyword, use_normalized)

        # Normalize the score by a scaling factor (can be tuned for balance)
        total_match_score /= len(keywords) * 3

        # Only keep results above the threshold
        if total_match_score >= threshold:
            ranked_results.append((book_id, total_match_score))

    # Sort results by match score in descending order
    ranked_results.sort(key=lambda x: x[1], reverse=True)

    # Validate matched book IDs against the `ids` table
    valid_ids = []
    detailed_results = []  # To store all results including duplicates

    for book_id, rank in ranked_results:
        # Fetch all matches for the current book_id
        cursor.execute("SELECT id FROM ids WHERE type = ?", (book_id,))
        matching_ids = cursor.fetchall()  # Fetch all matching rows

        # Treat each match independently
        for matching_id in matching_ids:
            valid_ids.append(matching_id[0])  # Append the ID
            detailed_results.append((matching_id[0], book_id, rank))  # Include additional details

    # Return valid book IDs and detailed results
    return valid_ids, detailed_results


def all_books(cursor):
    """
    Retrieve all book IDs with a fixed confidence score of 100.

    Parameters:
        cursor: Database cursor to execute SQL queries.

    Returns:
        A tuple containing:
        - A list of all valid book IDs.
        - A list of tuples (book_id, rank), where rank is fixed at 100.
    """
    # Fetch all IDs from the `ids` table
    cursor.execute("SELECT id FROM ids")
    matching_ids = cursor.fetchall()

    # Create valid IDs and fixed ranking
    valid_ids = [row[0] for row in matching_ids]
    ranked_results = [(book_id, 100) for book_id in valid_ids]

    return valid_ids, ranked_results


# Example usage
if __name__ == "__main__":
    import sqlite3
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    
    search_query = input("Enter book name or keywords: ")
    valid_ids, detailed_results = search_books(cursor, search_query)

    for valid_id, book_id, rank in detailed_results:
        print(f"Valid ID: {valid_id} | Book ID: {book_id} | Confidence: {rank}%")
