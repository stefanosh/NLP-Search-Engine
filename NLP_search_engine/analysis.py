import sqlite3
import nltk

conn = sqlite3.connect('database/crawler_db.sqlite')

cur = conn.cursor()
cur.execute("SELECT text FROM ARTICLES")

rows = cur.fetchall()
 
# Syntactic analysis and indexing from here and after..
for t in rows:
    text = t[0].lower()
    tokens = nltk.word_tokenize(text) 
    tags = nltk.pos_tag(text)


# Save (commit) the changes
conn.commit()  
conn.close()