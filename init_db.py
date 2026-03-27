import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("CREATE TABLE users (username TEXT, password TEXT)")
c.execute("CREATE TABLE notes (user TEXT, content TEXT)")

conn.commit()
conn.close()

print("Database created!")