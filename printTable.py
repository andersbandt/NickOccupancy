import sqlite3

conn = sqlite3.connect('data.db')
cur = conn.cursor()
print("Opened database successfully, attempting to print the contents")

with conn:
	cur.execute('''SELECT * FROM OCCUPANCY''')
	#conn.commit()
	print(cur.fetchall())

conn.close()
