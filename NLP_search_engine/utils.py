from nltk.corpus import wordnet

# remves stop words from list of words passed as argument in following structure: [("word1","the_tag"),("word2","the_tag")]


def removeStopWordsFromListOfWords(words):
    closedClassCategoriesTuple = ("CD", "CC", "DT", "EX", "IN", "LS", "MD", "PDT",
                                  "POS", "PRP",  "PRP",  "RP",   "TO", "UH", "WDT", "WP", "WP", "WRB")
    returnedWords = []
    for word in words:
        if word[1] not in closedClassCategoriesTuple:
            returnedWords.append(word)
    return returnedWords

# Return the correct pos_tag needed for lemmatizer, as it doesn't accept all tags


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
