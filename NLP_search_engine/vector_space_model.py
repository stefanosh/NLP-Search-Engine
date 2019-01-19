import json
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import numpy as np
from pprint import pprint
from pathlib import Path
import xml.etree.cElementTree as element_tree
from xml.dom import minidom
import sys

# calculates TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
# article is in json format, containing all the lemmas


def tf_of(word, article):
    times_t_in_article = 0
    for lemma in article:  # for every lemma in article
        if word == lemma["word"]:
            times_t_in_article += 1
    return(times_t_in_article / float(len(article)))

# calculates IDF(t) = log_e(Total number of documents / Number of documents with term t in it)
# **NOTE** changed here the return status, so that it also returns in which articles the word exists,
# so that we avoid this extra looops on later stage


def idf_of(word):
    number_of_docs_containing_word = 0
    ids_list = []
    for article in data["articles"]:
        for text_id in article:
            # for every word in every article
            for lemma in article[str(text_id)]:
                if(lemma["word"] == word):
                    number_of_docs_containing_word += 1
                    ids_list.append(text_id)
                    break

    return {"idf": np.log(articles_count / float(number_of_docs_containing_word)), "texts_ids": ids_list}

# hold only unique words in every article - remove duplicates


def removeDuplicateWordsFromEachArticle(data):
    dataToReturn = {"articles": []}
    for article in data["articles"]:
        for text_id in article:
            shown_list = []
            for word in article[str(text_id)]:
                if word not in shown_list:
                    for i in dataToReturn["articles"]:
                        if(str(text_id) in i):
                            dataToReturn["articles"][dataToReturn["articles"].index(
                                i)][str(text_id)].append(word)
                            break
                    else:
                        dataToReturn["articles"].append({str(text_id): [word]})
                    shown_list.append(word)
    return dataToReturn

# for every article it removes the stopwords, by creating a new array which holds all the values of


def removeStopWords(data):
    closedClassCategoriesTuple = ("CD", "CC", "DT", "EX", "IN", "LS", "MD", "PDT",
                                  "POS", "PRP",  "PRP",  "RP",   "TO", "UH", "WDT", "WP", "WP", "WRB")

    dataToReturn = {"articles": []}
    for article in data["articles"]:  # for every article:
        for text_id in article:
            # for every word in every article
            for word in article[str(text_id)]:
                if word["pos_tag"] not in closedClassCategoriesTuple:  # if the tag isn't closedclass
                    # hold the word, either by creating value for text_id, or if text_id already exists, add it to its values
                    # so that we have same structure as file created after posTagging
                    for i in dataToReturn["articles"]:
                        if(str(text_id) in i):
                            dataToReturn["articles"][dataToReturn["articles"].index(
                                i)][str(text_id)].append(word)
                            break
                    else:
                        dataToReturn["articles"].append({str(text_id): [word]})

    return dataToReturn

# Needed for calculation of tf*idf in each unique word, because in calculation of idf we calculate also the texts containing this unique word,
#  but we don't know at that point what is its tf


def get_tf_of_word_from_article(set_tf, word, article_id):
    key = str(article_id) + ":" + word
    return set_tf[key]

# Return the correct pos_tag needed for lemmatizer, as it doesn;t accept all tags


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.ADV


with open('texts_pos_tagged.json') as f:
    data = json.load(f)

articles_count = len((data["articles"]))
print("Total articles: " + str(articles_count))
allwords_set = set()

print('Removing stopwords...')
data = removeStopWords(data)


# Lemmatisation of words
print('Lemmatization...')
lemmatizer = WordNetLemmatizer()
for article in data["articles"]:
    for text_id in article:
            # for every word in every article
        for word in article[str(text_id)]:
            word["word"] = lemmatizer.lemmatize(
                word["word"], get_wordnet_pos(word["pos_tag"]))
            allwords_set.add(word["word"])

all_unique_words_count = len(allwords_set)
print("Total number of unique words: " + str(all_unique_words_count))


# calculate tf for every lemma and add it to set_tf
print('Calculating tf ')
set_tf = {}  # set_tf will contain as key the "article_id:word" ex: "12:start" and as value the tf of this word in the specified article
# in this way, we can use get_tf_of_word_from_article function which will return the tf of a given word for a given article immediately, without any loop.
for article in data["articles"]:
    for text_id in article:
            # for every word in every article
        for word in article[str(text_id)]:
            key = str(text_id)+":"+word["word"]
            set_tf[key] = tf_of(word["word"], article[str(text_id)])

print('Removing duplicates...')
# since we don't need duplicate words in each article anymore, we can remove them
data = removeDuplicateWordsFromEachArticle(data)


print('Calculating idf of unique set')
set_idf = {}
xml_dict = {}  # will contain every unique word, and foreach word, there will be an array containing the articles_ids it belongs and the idf per article
iteration = 0
for x in allwords_set:
    xml_dict[x] = []
    set_idf[x] = idf_of(x)
    # for every article containing this unique word, here it is also calculated the final tf*idf, so after it, xml_dict will be ready to be written on xml file immediately
    for article_id in set_idf[x]["texts_ids"]:
        xml_dict[x].append({str(article_id): set_idf[x]["idf"] *
                            get_tf_of_word_from_article(set_tf, x, article_id)})
    iteration += 1
    progress_per_cent = (float(iteration) / float(all_unique_words_count))*100
    sys.stdout.write("Calculating idf progess: %0.1f%%   \r" % (progress_per_cent) )
    sys.stdout.flush()

# with open(str(Path(__file__).parent) + '/inverted_index.json', 'w') as outfile:
#     json.dump(xml_dict, outfile)

#creation of inverted_index xml file
print("Writing to inverted_index.xml...")

root = element_tree.Element("inverted_index")

for lemma in xml_dict:
    xml_lemma = element_tree.SubElement(root, "lemma", name=lemma)
    for article in xml_dict[lemma]:
        for article_single in article:
            element_tree.SubElement(
                xml_lemma, "document", id=article_single, weight=str(article[article_single]))

tree = element_tree.ElementTree(root)

xmlstr = minidom.parseString(
    element_tree.tostring(root)).toprettyxml(indent="   ")
with open(str(Path(__file__).parent) + '/inverted_index.xml', "w") as outputfile:
    outputfile.write(xmlstr)