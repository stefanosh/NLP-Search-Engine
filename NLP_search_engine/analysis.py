import sqlite3
import nltk
nltk.download('all')

conn = sqlite3.connect('database/crawler_db.sqlite')

cur = conn.cursor()
cur.execute("SELECT text FROM ARTICLES")

rows = cur.fetchall()
 
# Syntactic analysis and indexing from here and after..
""" for t in rows:
    #print(t[0])
    text = t[0].lower()
    tokens = nltk.word_tokenize(text)  """
    



# Save (commit) the changes
conn.commit()  
conn.close()