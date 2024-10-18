import sqlite3
import os
import time  # For Unix timestamp handling
import random
import string

try:
    from prettytable import PrettyTable
except ImportError:
    os.system("pip install prettytable")
    from prettytable import PrettyTable

def id_generate(size, allowed_chars : str):
    return ''.join(random.choice(allowed_chars) for x in range(size)) 

# Ten CSDL
db_name = "data"

# Ket noi vao CSDL SQLite
db = sqlite3.connect(f"{db_name}.db")

# Tao mot vat the de chay lenh SQL
cursor = db.cursor()

# Tao mot TABLE neu TABLE ids ko ton tai
cursor.execute('''
    CREATE TABLE IF NOT EXISTS  ids (
        id TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL,
        donor TEXT NOT NULL,
        donateday INTEGER NOT NULL
    )
''')

# Retrieve and display data using PrettyTable
cursor.execute('SELECT * FROM  ids')
rows = cursor.fetchall()

# Print the data in a pretty table
table = PrettyTable()
table.field_names = ["ID", "Type", "Donor", "Day of donation"]

# Add rows to the PrettyTable
for row in rows:
    table.add_row(row)

# Display the table
print(table)

ntype=str(input("Enter type of new item (BLANK IF IGNORE): "))
if (ntype != ""):
    nid = str(input("Enter id of new book (BLANK IF RANDOMIZED): "))
    if nid == "": nid = id_generate(11, string.ascii_letters+string.digits)
    print(f"New ID: [{nid}]")
    donor = str(input("Enter donator: "))


    # Insert sample data using current time for `borrow_day` and future time for `borrow_expire`
    current_time = int(time.time())  # Get current Unix timestamp

    data = (nid, ntype, donor, current_time)

    # Insert data into the table
    cursor.execute('''
        INSERT OR IGNORE INTO  ids (id, type, donor, donateday)
        VALUES (?, ?, ?, ?)
    ''', data)

# Commit the transaction and close the connection
db.commit()

# Close the database connection
db.close()
