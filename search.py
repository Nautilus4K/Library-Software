from os import system as cmd
try: from fuzzywuzzy import fuzz
except ImportError:
    cmd("pip install fuzzywuzzy")
    from fuzzywuzzy import fuzz
import unicodedata

# Function to normalize and remove accents
def normalize_unicode(text):
    # Normalize to NFKD form and remove diacritics/accents by filtering combining characters
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

def search_books(cursor, search_query : str, threshold=40):
    # Normalize the search query and split it into keywords
    keywords = normalize_unicode(search_query.lower()).split()

    # SQL query to get both `id` and `title` from the `books` table
    cursor.execute("SELECT id, title FROM books")
    all_titles = cursor.fetchall()  # Fetch all rows as a list of tuples (id, title)

    # Debug: Print out all titles fetched
    # print(f"Fetched {len(all_titles)} titles from 'books' table.")

    # A list to store tuples of (id, rank)
    ranked_results = []

    # Loop through each row in the `books` table
    for book_id, title in all_titles:
        # Normalize the title for case-insensitive and accent-insensitive comparison
        title_normalized = normalize_unicode(title.lower())

        # Initialize total match score for the current title
        total_match_score = 0

        # Fuzzy matching for each keyword in the query
        for keyword in keywords:
            # Apply fuzzy matching for keyword vs normalized title
            match_score = fuzz.partial_ratio(keyword, title_normalized)
            
            # Add to total match score if above a certain threshold
            if match_score >= threshold:
                total_match_score += match_score

        # Only consider titles that have at least one match above the threshold
        if total_match_score > 0:
            ranked_results.append((book_id, total_match_score))

    # Debug: Print out the ranked results before filtering
    # print(f"Ranked Results (before filtering with 'ids'): {ranked_results}")

    # Sort the results by total match score in descending order
    ranked_results.sort(key=lambda x: x[1], reverse=True)

    # Loop through each matched book id and check if it exists in the `ids` table with the same `type`
    valid_ids = []
    for book_id, _ in ranked_results:
        # Check if this `book_id` exists in the `ids` table with the same `type`
        cursor.execute("SELECT id FROM ids WHERE type = ?", (book_id,))
        matching_id = cursor.fetchone()

        # Debug: Show each query result
        # print(f"Checking id {book_id} in 'ids' table: {matching_id}")

        # If a match is found in the `ids` table, store the `id`
        if matching_id:
            valid_ids.append(matching_id[0])

    return [valid_ids, ranked_results]

def all_books(cursor):
    """
    Retrieve all books that have the specified format and return them with a confidence score of 100.

    Parameters:
    - cursor: Database cursor for executing SQL queries.
    - format_id: The format ID to match in the `ids` table.

    Returns:
    - A list of valid book IDs.
    - A list of tuples (id, rank) with rank fixed at 100 for each matched book.
    """
    # Query the `ids` table to get all book IDs with the specified format type
    cursor.execute("SELECT id FROM ids")
    matching_ids = cursor.fetchall()

    # Extract book IDs from the fetched rows
    valid_ids = [row[0] for row in matching_ids]

    # Assign a rank of 100 to each book in the `ranked_results`
    ranked_results = [(book_id, 100) for book_id in valid_ids]

    return valid_ids, ranked_results


# Example usage
if __name__ == "__main__":
    import sqlite3
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    
    search_query = input("Enter book name or keywords: ")
    ids = search_books(cursor, search_query)
    for i in range(len(ids[0])):
        valid_id = ids[0][i]
        bktype = ids[1][i][0]
        rank = ids[1][i][1]
        print(f"id: {valid_id} | type: {bktype} | confidence: {rank}%")
