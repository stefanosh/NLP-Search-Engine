import sqlite3
from pathlib import Path

conn = sqlite3.connect(str(Path(__file__).parent) + '/crawler_db.sqlite')

cursor = conn.cursor()
cursor.execute('''DROP TABLE IF EXISTS ARTICLES''')
cursor.execute('''CREATE TABLE ARTICLES (
                                id INTEGER PRIMARY KEY,
                                title TEXT NOT NULL ,
                                url TEXT NOT NULL UNIQUE,
                                text NOT NULL UNIQUE);''')


# Save (commit) the changes
conn.commit()
conn.close()
