import argparse
from xmljson import badgerfish
from xml.etree.ElementTree import fromstring
import xml.etree.ElementTree as ET
from json import dumps, loads
from pprint import pprint
# Read one or more words from the command line
parser = argparse.ArgumentParser(description='Quering the database')
parser.add_argument('words', metavar='word_name', type=str, nargs='+',
                    help='The word with which you make a search request. You can add multiple words with space between.')

args = parser.parse_args()

# read inverted_index and load to dictionary
tree = ET.parse('inverted_index.xml')
root = tree.getroot()
xmlstr = ET.tostring(root, encoding='utf8', method='xml')

# dumps converts data to json string and loads converts to json
jsonObj = loads(dumps(badgerfish.data(fromstring(xmlstr))))

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


requestedWordsList = getListOfDocsWithWeightsForWords(args.words)

# param wordsListWithArticleIds has all words included in query with corresponding ids and weights, but without the addition of weights of document_ids which have multiple words of the query inside their words.
# getSumOfWeightsForArticlesWithSameWords returns an array which isn;t divided in each word, but with unique ids and added weight values for each id which had multiple words matched


def getSumOfWeightsForArticlesWithSameWords(wordsListWithArticleIds):
    if(len(wordsListWithArticleIds) > 0):
        dictc = wordsListWithArticleIds[0]["document"]
        for i in range(1, len(wordsListWithArticleIds)):
            for j in wordsListWithArticleIds[i]["document"]:
                flag = 1
                for last in dictc:
                    if(j["@id"] == last["@id"]):
                        last["@weight"] += j["@weight"]
                        flag = 0
                        break
                if flag:
                    dictc.append(j)
    else:
        dictc = []
    return dictc


finalListWithIdsAfterQuery = getSumOfWeightsForArticlesWithSameWords(
    requestedWordsList)
if len(finalListWithIdsAfterQuery) > 0:
    pprint(finalListWithIdsAfterQuery)
else:
    print("No article matches your search query")
