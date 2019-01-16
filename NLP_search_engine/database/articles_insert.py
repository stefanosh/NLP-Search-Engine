import sqlite3
import json

conn = sqlite3.connect('crawler_db.sqlite',timeout=10)
cursor = conn.cursor()

with open('../spiders/hackernews.json') as json_file:  
    data = json.load(json_file)
    for row in data:
        cursor.execute('''INSERT INTO ARTICLES (title,url,text) 
                          VALUES (?,?,?)''',
                          (row['text-title'],row['text-url'],row['text-content']))

with open('../spiders/technews.json') as json_file:  
    data = json.load(json_file)
    for row in data:
        cursor.execute('''INSERT INTO ARTICLES (title,url,text) 
                          VALUES (?,?,?)''',
                          (row['text-title'],row['text-url'],row['text-content'])) 

# Save (commit) the changes
conn.commit()  
conn.close()