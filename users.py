import sqlite3
import os
import time  # For Unix timestamp handling
import random
import string
from hashlib import sha256

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

# Tao mot TABLE neu TABLE ids ko ton tai
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        name TEXT,
        date_created INTEGER,
        phone TEXT
    )
''')

# Retrieve and display data using PrettyTable
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

# Print the data in a pretty table
table = PrettyTable()
table.field_names = ["Username", "Password", "Name", "Date created", "Phone number"]

# Add rows to the PrettyTable
for row in rows:
    table.add_row(row)

# Display the table
print(table)

nusername=str(input("Enter new username (BLANK IF IGNORE): "))
if (nusername != ""):
    npasswd = sha256(str(input("Enter password: ")).encode("utf-8")).hexdigest()
    nname = str(input("Enter new name (BLANK IF NULL): "))
    if nname == "": nname = None
    nphone = str(input("Enter phone number (BLANK IF NULL): "))
    if nphone == "": nphone = None
    data = (nusername, npasswd, nname, int(time.time()), nphone)

    # Insert data into the table
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, name, date_created, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', data)

    db.commit()

remove = str(input("Enter username of user you want to remove (BLANK IF IGNORE): "))
if remove != "":
    cursor.execute("DELETE FROM users WHERE username=?", (remove,))

# Commit the transaction and close the connection
db.commit()

# Close the database connection
db.close()