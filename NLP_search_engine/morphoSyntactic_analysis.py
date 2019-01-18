import sqlite3
import nltk
import string
import json

# Propably needed before running the script
# nltk.download('all')

# This script performs the morphosyntactic analysis of articles
# Tokenization, pos tagging of every word in each article and creation of json file with this pos tagged data, to be used in vector_space_model.py


conn = sqlite3.connect('database/crawler_db.sqlite')

cur = conn.cursor()
cur.execute("SELECT text FROM ARTICLES LIMIT 200")

rows = cur.fetchall()
data = {}
tmp = {}
data["articles"] = []
article_id = 0

# For every article in database perform the following operations
for row in rows:   
    text = row[0].lower()
    tokens = nltk.word_tokenize(text) 
    tags = nltk.pos_tag(tokens)
    article_id = article_id + 1
    
    tmp = {}
    tmp[article_id] = []
    # For every pos tag tuple (word,pos tag)
    for t in tags:
        tmp[article_id].append({  
                            "word": t[0],
                            "pos_tag": t[1]
                            })

    data["articles"].append(tmp)

with open('texts_pos_tagged_200.json', 'w') as outfile:  
    json.dump(data, outfile) 
 

# Save (commit) the changes
conn.commit()  
conn.close() 

