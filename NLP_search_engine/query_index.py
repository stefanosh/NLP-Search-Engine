import argparse
from xmljson import badgerfish
from xml.etree.ElementTree import fromstring
import xml.etree.ElementTree as ET
from json import dumps, loads
from pprint import pprint

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
        if(isinstance(wordsListWithArticleIds[0]["document"], list)): # this handle needed because if first word exists only in one document, wordsListWithArticleIds[0]["document"] is not a list, and then new elements cant be appended, so must be manually added in a list
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

# dumps converts data to json string and loads converts to json
jsonObj = loads(dumps(badgerfish.data(fromstring(xmlstr))))

requestedWordsList = getListOfDocsWithWeightsForWords(args.words)

finalListWithIdsAfterQuery = getSumOfWeightsForArticlesWithSameWords(
    requestedWordsList)

if len(finalListWithIdsAfterQuery) > 0:
    finalListWithIdsAfterQuery.sort(key=lambda x: x["@weight"], reverse=True)
    if(args.limit == None): #if no limit specified then display all relevant articles
        pprint(finalListWithIdsAfterQuery)
    else:
        iterations = min(args.limit, len(finalListWithIdsAfterQuery))
        for i in range(0, iterations):
            print(finalListWithIdsAfterQuery[i])

else:
    print("No article matches your search query")
