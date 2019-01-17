import json
from nltk.stem import WordNetLemmatizer
import numpy as np
from pprint import pprint
# calculates TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
# article is in json format, containing all the lemmas


def tf_of(word, article):
    times_t_in_article = 0
    total_words_in_article = 0
    for lemma in article:  # for every lemma in article
        if word == lemma["word"]:
            times_t_in_article += 1
        total_words_in_article += 1
    return(times_t_in_article / float(total_words_in_article))

# calculates IDF(t) = log_e(Total number of documents / Number of documents with term t in it)


def idf_of(word, data):
    total_number_of_docs = 0
    number_of_docs_containing_word = 0
    for article in data["articles"]:
        for text_id in article:
            # for every word in every article
            for lemma in article[str(text_id)]:
                if(lemma["word"] == word):
                    number_of_docs_containing_word += 1
                    break
        total_number_of_docs += 1
    return np.log(total_number_of_docs / float(number_of_docs_containing_word))

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


with open('withpos.json') as f:
    data = json.load(f)

data = removeStopWords(data)

# Lemmatisation of words
lemmatizer = WordNetLemmatizer()
for article in data["articles"]:
    for text_id in article:
            # for every word in every article
        for word in article[str(text_id)]:
            word["word"] = lemmatizer.lemmatize(
                word["word"], pos=word["pos_tag"].lower())

# calculate tf for every lemma and add it to json object
for article in data["articles"]:
    for text_id in article:
            # for every word in every article
        for word in article[str(text_id)]:
            word["tf"] = tf_of(word["word"], article[str(text_id)])

#since we don't need duplicate words in each article anymore, we can remove them
data = removeDuplicateWordsFromEachArticle(data)

# calculate idf (and tf*idf in the same time) for every lemma and add it to json object
for article in data["articles"]:
    for text_id in article:
            # for every word in every article
        for word in article[str(text_id)]:
            word["idf"] = idf_of(word["word"], data)
            word["tf_idf"] = word["idf"] * word["tf"]

pprint(data)
