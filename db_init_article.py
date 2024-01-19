import sqlite3

conn = sqlite3.connect('articles.db')
cur = conn.cursor()

# testing data
cur.execute('DROP TABLE IF EXISTS articles')

cur.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, content BLOB NOT NULL, created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP        )')

cur.execute(
    'INSERT INTO articles (title, content) VALUES (?, ?)',
    ('test_1', 'a quick brown fox jumps over the lazy dog')
)

cur.execute(
    'INSERT INTO articles (title, content) VALUES (?, ?)',
    ('test_2', 'another quick brown fox jumps over the lazy dog')
)

# commit and close
conn.commit()
conn.close()