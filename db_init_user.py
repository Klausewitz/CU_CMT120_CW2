import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()

# testing data
cur.execute(
    'DROP TABLE IF EXISTS users'
)

cur.execute('CREATE TABLE IF NOT EXISTS `users` (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL);')

cur.execute(
    'INSERT INTO users (username, password) VALUES (?, ?)',
    ('Admin', '$2b$12$zG2S2UKq7cihFnKQXwNBtuxP9PA8M87VUeNMW/XdhCYLi7Lwnwx4C')
)


# commit and close
conn.commit()
conn.close()