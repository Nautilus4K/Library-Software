import sqlite3
import os
import time  # For Unix timestamp handling

try:
    from prettytable import PrettyTable
except ImportError:
    os.system("pip install prettytable")
    from prettytable import PrettyTable

# Ten CSDL
db_name = "data"

# Ket noi vao CSDL SQLite
db = sqlite3.connect(f"{db_name}.db")

# Tao mot vat the de chay lenh SQL
cursor = db.cursor()

# Tao mot TABLE neu TABLE books ko ton tai
cursor.execute('''
    CREATE TABLE IF NOT EXISTS  books (
        id TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        description TEXT NOT NULL,
        use TEXT NOT NULL
    )
''')

# Retrieve and display data using PrettyTable
cursor.execute('SELECT * FROM  books')
rows = cursor.fetchall()

# Print the data in a pretty table
table = PrettyTable()
table.field_names = ["ID", "Title", "Author", "Year", "Description", "Use"]

maxcharlimit = 25
# Add rows to the PrettyTable
for row in rows:
    # Assuming row is a tuple
    row = tuple(str(item[:maxcharlimit-3]) + "..." if len(str(item)) > maxcharlimit else item for item in row)
    table.add_row(row)


# Display the table
print(table)

nbook=str(input("Enter title of new book (BLANK IF IGNORE): "))
if (nbook != ""):
    nid = str(input("Enter id of new book: "))
    nauthor = str(input("Enter author: "))
    year = str(input("Enter year of book: "))
    desc = str(input("Enter description: "))
    use = str(input("Enter use of new book: "))

    # Insert sample data using current time for `borrow_day` and future time for `borrow_expire`
    current_time = int(time.time())  # Get current Unix timestamp
    expire_time = current_time + 7 * 24 * 60 * 60  # Borrow period of 7 days from now

    data = (nid, nbook, nauthor, year, desc, use)

    # Insert data into the table
    cursor.execute('''
        INSERT OR IGNORE INTO  books (id, title, author, year, description, use)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)

# Commit the transaction and close the connection
db.commit()

# Close the database connection
db.close()
