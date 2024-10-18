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
    CREATE TABLE IF NOT EXISTS  borrows (
        id TEXT NOT NULL UNIQUE,
        current_borrower TEXT NOT NULL,
        borrow_day INTEGER,  -- Unix timestamp (integer)
        borrow_expire INTEGER NOT NULL  -- Unix timestamp for expiration (integer)
    )
''')

# Retrieve and display data using PrettyTable
cursor.execute('SELECT * FROM  borrows')
rows = cursor.fetchall()

# Print the data in a pretty table
table = PrettyTable()
table.field_names = ["ID", "Current Borrower", "Borrow Day (Unix)", "Borrow Expire (Unix)"]

# Add rows to the PrettyTable
for row in rows:
    table.add_row(row)

# Display the table
print(table)

nid=str(input("Enter id of new borrow (BLANK IF IGNORE): "))
if (nid != ""):
    cursor.execute('SELECT type FROM ids WHERE id=?', (nid,))
    name = cursor.fetchone()[0]
    cursor.execute('SELECT title FROM books WHERE id=?', (name,))
    name = cursor.fetchone()[0]
    print("Targeted book: "+name)
    nborrower = str(input("Name of borrower: "))

    # Insert sample data using current time for `borrow_day` and future time for `borrow_expire`
    current_time = int(time.time())  # Get current Unix timestamp
    expire_time = current_time + 7 * 24 * 60 * 60  # Borrow period of 7 days from now

    data = (nid, nborrower, current_time, expire_time)

    # Insert data into the table
    cursor.execute('''
        INSERT OR IGNORE INTO  borrows (id, current_borrower, borrow_day, borrow_expire)
        VALUES (?, ?, ?, ?)
    ''', data)

# Commit the transaction and close the connection
db.commit()

# Close the database connection
db.close()
