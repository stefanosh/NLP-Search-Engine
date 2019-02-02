import argparse
from xmljson import badgerfish
from xml.etree.ElementTree import fromstring
import xml.etree.ElementTree as ET
from json import dumps, loads
from pprint import pprint
import nltk
from nltk.stem import WordNetLemmatizer
import utils
import sqlite3
from pathlib import Path

import time
start_time = time.time()
# pass words and it returns all docs and weights for each word in a list


def getListOfDocsWithWeightsForWords(words):
    wordsFoundCount = 0  # this variable is used so that for loop breaks after we found for each word its entry, so that it doesn't continue looping for all other words left
    dicts = []
    numberOfWords = len(words)
    for index in jsonObj["inverted_index"]["lemma"]:
        if(index["@name"] in words):
            dicts.append(index)

            wordsFoundCount += 1
            if(wordsFoundCount == numberOfWords):
                break
    return dicts


# param wordsListWithArticleIds has all words included in query with corresponding ids and weights, but without the addition of weights of document_ids which have multiple words of the query inside their words.
# getSumOfWeightsForArticlesWithSameWords returns an array which isn;t divided in each word, but with unique ids and added weight values for each id which had multiple words matched


def getSumOfWeightsForArticlesWithSameWords(wordsListWithArticleIds):
    if(len(wordsListWithArticleIds) > 0):
        # this handle needed because if first word exists only in one document, wordsListWithArticleIds[0]["document"] is not a list, and then new elements cant be appended, so must be manually added in a list
        if(isinstance(wordsListWithArticleIds[0]["document"], list)):
            dictc = wordsListWithArticleIds[0]["document"]
        else:
            dictc = [wordsListWithArticleIds[0]["document"]]

        for i in range(1, len(wordsListWithArticleIds)):
            # this handle needed because if a word exists only in one document, wordsListWithArticleIds[i]["document"] is not a list, so for in loop crashes
            if(isinstance(wordsListWithArticleIds[i]["document"], list)):
                for j in wordsListWithArticleIds[i]["document"]:
                    flag = 1
                    for last in dictc:
                        if(j["@id"] == last["@id"]):
                            last["@weight"] += j["@weight"]
                            flag = 0
                            break
                    if flag:
                        dictc.append(j)
            # when wordsListWithArticleIds[i]["document"] is not a list and should not get in previous for j in loop
            else:
                dictc.append(wordsListWithArticleIds[i]["document"])
    else:
        dictc = []
    return dictc


# Read one or more words from the command line
parser = argparse.ArgumentParser(description='Quering the database')
parser.add_argument('words', metavar='word_name', type=str, nargs='+',
                    help='The word with which you make a search request. You can add multiple words with space between.')
parser.add_argument('--limit', metavar='number', type=int,
                    help='Limit the number of articles displayed. By default all articles matched are returned')
args = parser.parse_args()

# read inverted_index and load to dictionary
tree = ET.parse('inverted_index.xml')
root = tree.getroot()
xmlstr = ET.tostring(root, encoding='utf8', method='xml')

# dumps function converts data to json string and loads function converts to json
# *NOTE:* most time consuming operation in 25 articles was below line and lemmatize step, rather than the query calculation afterwards
jsonObj = loads(dumps(badgerfish.data(fromstring(xmlstr))))

# lowercase the search query
for i in range(0, len(args.words)):
    args.words[i] = args.words[i].lower()

# add tags and remove stopWords
wordsWithTagsAndStopWords = nltk.pos_tag(args.words)
wordsWithTags = utils.removeStopWordsFromListOfWords(wordsWithTagsAndStopWords)

# leammatize words and remove the tag, in order to be ready for query
lemmatizer = WordNetLemmatizer()
words = []
for i in range(0, len(wordsWithTags)):
    words.append(lemmatizer.lemmatize(
        wordsWithTags[i][0], utils.get_wordnet_pos(wordsWithTags[i][1])))

# get the articles containing the words of the query and add weights if articles contain multiple words of the query
docsContainingRequestedWords = getListOfDocsWithWeightsForWords(words)
finalListWithIdsAfterQuery = getSumOfWeightsForArticlesWithSameWords(
    docsContainingRequestedWords)

# display results
if len(finalListWithIdsAfterQuery) > 0:
    conn = sqlite3.connect(str(Path(__file__).parent) +
                           '/database/crawler_db.sqlite')

    cursor = conn.cursor()

    finalListWithIdsAfterQuery.sort(key=lambda x: x["@weight"], reverse=True)
    if(args.limit == None):  # if no limit specified then display all relevant articles
        # pprint(finalListWithIdsAfterQuery)
        iterations = len(finalListWithIdsAfterQuery)
    else:
        iterations = min(args.limit, len(finalListWithIdsAfterQuery))
    for i in range(0, iterations):
        id = finalListWithIdsAfterQuery[i]["@id"]
        cursor.execute(
            "SELECT url,title FROM ARTICLES WHERE id=?", (str(id),))

        rows = cursor.fetchall()
        print(str(i+1)+". " + rows[0][1]+"\n"+rows[0][0]+"\n" +
              "With weight: "+str(finalListWithIdsAfterQuery[i]["@weight"])+"\n")
        # print(finalListWithIdsAfterQuery[i]["@id"])
    conn.commit()
    conn.close()
else:
    print("No article matches your search query")
print("--- Total time in seconds: %s---" % (time.time() - start_time))