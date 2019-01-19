import sqlite3
import nltk
import string
import json
from pprint import pprint
from pathlib import Path

# Propably needed before running the script
# nltk.download('all')

# This script performs the morphosyntactic analysis of articles
# Tokenization, pos tagging of every word in each article and creation of json file with this pos tagged data, to be used in vector_space_model.py

print("Adding pos tags...")
conn = sqlite3.connect(str(Path(__file__).parent) +
                       '/database/crawler_db.sqlite')

cursor = conn.cursor()
cursor.execute("SELECT id,text FROM ARTICLES")

data = {}
tmp = {}
data["articles"] = []

# For every article in database perform the following operations
for row in cursor:
    text = row[1].lower()
    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)

    tmp = {}
    tmp[row[0]] = []
    # For every pos tag tuple (word,pos tag)
    for t in tags:
        tmp[row[0]].append({
            "word": t[0],
            "pos_tag": t[1]
        })

    data["articles"].append(tmp)

with open(str(Path(__file__).parent) + '/texts_pos_tagged.json', 'w') as outfile:
    json.dump(data, outfile)

# Save (commit) the changes
conn.commit()
conn.close()
