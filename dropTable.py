import sqlite3

conn = sqlite3.connect('data.db')
print("Opened database successfully")

conn.execute('''DROP TABLE OCCUPANCY''')

print("Table dropped successfully")

conn.close()
