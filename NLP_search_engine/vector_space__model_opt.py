import json
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import numpy as np
from pprint import pprint

# calculates TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
# article is in json format, containing all the lemmas


def tf_of(word, article):
    times_t_in_article = 0
    for lemma in article:  # for every lemma in article
        if word == lemma["word"]:
            times_t_in_article += 1      
    return(times_t_in_article / float(len(article)))

# calculates IDF(t) = log_e(Total number of documents / Number of documents with term t in it)


def idf_of(word):
    number_of_docs_containing_word = 0
    for article in data["articles"]:
        for text_id in article:
            # for every word in every article
            for lemma in article[str(text_id)]:
                if(lemma["word"] == word):
                    number_of_docs_containing_word += 1
                    break
        
    return np.log(articles_count / float(number_of_docs_containing_word))

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


def get_wordnet_pos(tag):
    if  tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.ADV


with open('texts_pos_tagged_200.json') as f:
    data = json.load(f)

articles_count = len((data["articles"]))
print(articles_count)
allwords_set = set()

print('Remove stopwords')
data = removeStopWords(data)

print('Lemmatization')
# Lemmatisation of words
lemmatizer = WordNetLemmatizer()
for article in data["articles"]:
    for text_id in article:
            # for every word in every article
        for word in article[str(text_id)]:
            word["word"] = lemmatizer.lemmatize(
                word["word"], get_wordnet_pos(word["pos_tag"]))
            allwords_set.add(word["word"])

print(len(allwords_set))

print('Calculating tf ')
# calculate tf for every lemma and add it to json object
for article in data["articles"]:
    for text_id in article:
            # for every word in every article
        for word in article[str(text_id)]:
            word["tf"] = tf_of(word["word"], article[str(text_id)])


print('Remove duplicates')
#since we don't need duplicate words in each article anymore, we can remove them
data = removeDuplicateWordsFromEachArticle(data)

print('Calculating idf of unique set')
set_idf = {}
iteration = 0
for x in allwords_set:
    set_idf[x] = idf_of(x)
    iteration += 1
    print("Iteration: %d" % (iteration))


print(len(set_idf))

print('Calculating tf idf')
# calculate idf (and tf*idf in the same time) for every lemma and add it to json object
for article in data["articles"]:
    for text_id in article:
            # for every word in every article
        for word in article[str(text_id)]:
            word["idf"] = set_idf[word["word"]]
            word["tf_idf"] = word["idf"] * word["tf"]

pprint(data)

with open('vector_space_200.json', 'w') as outfile:  
    json.dump(data, outfile) 
 