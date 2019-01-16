import sqlite3


conn = sqlite3.connect('crawler_db.sqlite')

cursor = conn.cursor()
cursor.execute('''CREATE TABLE ARTICLES (
                                id INTEGER PRIMARY KEY,
                                title TEXT NOT NULL ,
                                url TEXT NOT NULL UNIQUE,
                                text NOT NULL UNIQUE);''')


# Save (commit) the changes
conn.commit()  
conn.close()