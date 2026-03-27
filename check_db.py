import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

print("USERS TABLE:")
for row in c.execute("SELECT * FROM users"):
    print(row)

conn.close()