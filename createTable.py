import sqlite3

conn = sqlite3.connect('data.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE OCCUPANCY
		(ID INTEGER PRIMARY KEY AUTOINCREMENT,
		DATETIME    TEXT    NOT NULL,
		OCCUPANCY   INT     NUL NULL);''')

print("Table created successfuly")

conn.close()
